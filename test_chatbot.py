# test_chatbot.py
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import torch
import re
from datetime import datetime

class SimpleCardBot:
    def __init__(self, training_file='training_data.json'):
        # Load training data
        with open(training_file, 'r', encoding='utf-8') as f:
            self.training_data = json.load(f)
        
        # Initialize vectorizer
        self.vectorizer = TfidfVectorizer()
        
        # Prepare questions and answers
        self.questions = [qa['question'] for qa in self.training_data['qa_pairs']]
        self.answers = [qa['answer'] for qa in self.training_data['qa_pairs']]
        
        # Fit vectorizer
        self.question_vectors = self.vectorizer.fit_transform(self.questions)
    
    def get_answer(self, user_question):
        # Vectorize user question
        question_vector = self.vectorizer.transform([user_question])
        
        # Calculate similarities
        similarities = cosine_similarity(question_vector, self.question_vectors)
        
        # Get most similar question index
        most_similar_idx = np.argmax(similarities)
        similarity_score = similarities[0][most_similar_idx]
        
        if similarity_score < 0.3:  # Threshold for similarity
            return "Xin lỗi, tôi không hiểu câu hỏi của bạn."
        
        return {
            "answer": self.answers[most_similar_idx],
            "similar_question": self.questions[most_similar_idx],
            "similarity": float(similarity_score)
        }

class EnhancedCardBot(SimpleCardBot):
    def __init__(self):
        super().__init__()
        self.encoder = SentenceTransformer('vinai/phobert-base')
        self.tokenizer = AutoTokenizer.from_pretrained('vinai/phobert-base')
        self.conversation_history = []
        self.context = {
            "current_card": None,
            "last_intent": None,
            "questions_asked": []
        }
        
        # Thêm danh sách thẻ
        self.available_cards = [
            "HDBank Vietjet Platinum",
            "HDBank Petrolimex 4in1",
            "HDBank Vietjet Classic",
            "HDBank Priority Visa Signature",
            "HDBank JCB Ultimate",
            "HDBank Best Friend Forever",
            "HDBank Visa Gold",
            "HDBank Visa Classic",
            "HDBank Mastercard Standard",
            "HDBank Mastercard Platinum",
            "HDBank Mastercard World",

        ]

        # Add support responses
        self.support_responses = {
            "initial": "Xin chào! Tôi có thể tư vấn cho bạn về các loại thẻ sau:\n" + \
                      "\n".join([f"{idx+1}. Thẻ {card}" for idx, card in enumerate(self.available_cards)]) + \
                      "\n\nBạn có thể chọn số thứ tự thẻ hoặc hỏi trực tiếp về thẻ bạn quan tâm.",
            "ask_card": "Bạn muốn tìm hiểu về thẻ nào? Vui lòng chọn số thứ tự hoặc tên thẻ.",
            "invalid_number": "Số thứ tự không hợp lệ. Vui lòng chọn số từ 1 đến {}"
        }

        # Enhanced intent patterns
        self.intents = {
            "greeting": [
                "xin chào", "chào", "hi", "hello", "hey", "chào bạn"
            ],
            "farewell": [
                "tạm biệt", "goodbye", "bye", "cảm ơn", "hẹn gặp lại"
            ],
            "card_info": [
                "thẻ", "hdbank", "visa", "jcb", "mastercard", 
                "thông tin", "loại thẻ", "sản phẩm"
            ],
            "benefits": [
                "lợi ích", "ưu đãi", "quyền lợi", "tính năng",
                "được gì", "có những gì", "điểm thưởng", "hoàn tiền",
                "miễn phí", "chiết khấu"
            ],
            "requirements": [
                "yêu cầu", "điều kiện", "cần gì", "thủ tục",
                "giấy tờ", "duyệt", "mở thẻ", "đăng ký", "làm thẻ",
                "thời gian", "bao lâu"
            ],
            "fees": [
                "phí", "lãi suất", "chi phí", "trả góp", "phạt",
                "thường niên", "phí phạt", "trả chậm", "trễ hạn",
                "bao nhiêu"
            ],
            "support": [
                "giúp đỡ", "hỗ trợ", "tư vấn", "hướng dẫn",
                "cần hỗ trợ", "muốn biết"
            ]
        }
        
        # Add multi-intent patterns
        self.multi_intent_patterns = [
            ["benefits", "fees"],
            ["requirements", "benefits"],
            ["card_info", "benefits"],
            ["card_info", "fees"]
        ]
        
        self.responses = {
            "greeting": [
                "Xin chào! Tôi là trợ lý HDBank, rất vui được giúp đỡ bạn.",
                "Chào bạn! Tôi có thể tư vấn gì về sản phẩm thẻ HDBank?",
                "Xin chào quý khách! Tôi có thể giúp gì cho bạn?",
                "Chào mừng bạn đến với HDBank! Bạn cần tư vấn về sản phẩm nào?"
            ],
            "farewell": [
                "Cảm ơn bạn đã quan tâm đến sản phẩm của HDBank. Chúc bạn một ngày tốt lành!",
                "Rất vui được tư vấn cho bạn. Hẹn gặp lại bạn lần sau!",
                "Cảm ơn bạn đã chat với tôi. Nếu cần hỗ trợ thêm, hãy quay lại nhé!",
                "Tạm biệt và chúc bạn một ngày vui vẻ!"
            ]
        }

    def preprocess_text(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        # Add more Vietnamese-specific normalization if needed
        return text

    def get_semantic_similarity(self, text1, text2):
        # Use sentence embeddings for better matching
        emb1 = self.encoder.encode(text1)
        emb2 = self.encoder.encode(text2)
        return cosine_similarity([emb1], [emb2])[0][0]
        
    def get_intent(self, text):
        text = text.lower()
        
        # Check for multiple intents first
        found_intents = []
        for intent, patterns in self.intents.items():
            if any(pattern in text for pattern in patterns):
                found_intents.append(intent)
        
        # If multiple intents found, check if it matches known combinations
        if len(found_intents) > 1:
            for combo in self.multi_intent_patterns:
                if all(intent in found_intents for intent in combo):
                    return "multi_intent"
        
        # For single intent, use semantic similarity
        max_similarity = 0
        chosen_intent = "general_query"
        
        for intent, patterns in self.intents.items():
            for pattern in patterns:
                similarity = self.get_semantic_similarity(text, pattern)
                if similarity > max_similarity:
                    max_similarity = similarity
                    chosen_intent = intent
        
        return chosen_intent
        
    def get_card_metadata(self, question):
        # Dummy implementation, replace with actual logic
        return {"card_name": "HDBank Card"}

    def format_response(self, answer, intent, metadata=None):
        # Handle greetings and farewells specially
        if intent == "greeting":
            return np.random.choice(self.responses["greeting"])
        elif intent == "farewell":
            return np.random.choice(self.responses["farewell"])
            
        # Handle other intents
        if intent in self.responses:
            return np.random.choice(self.responses[intent])
        
        return answer
        
    def get_answer(self, user_input: str) -> str:
        # Preprocess input
        text = self.preprocess_text(user_input)
        intent = self.get_intent(text)

        # Handle support requests
        if any(phrase in text.lower() for phrase in ["cần hỗ trợ", "tư vấn", "giúp đỡ"]):
            if not any(card.lower() in text.lower() for card in self.available_cards):
                return self.support_responses["initial"]

        # Handle card number selection
        if text.startswith(tuple(str(i) for i in range(1, len(self.available_cards) + 1))):
            selected_card = self.get_card_by_number(text.split()[0])
            if selected_card:
                self.context["current_card"] = selected_card
                # Get card description from training data
                card_info = self.get_card_info(selected_card)
                return f"Thông tin về {selected_card}:\n{card_info}"
            else:
                return self.support_responses["invalid_number"].format(len(self.available_cards))

        # Check if question is about a specific card
        mentioned_card = None
        for card in self.available_cards:
            if card.lower() in text.lower():
                mentioned_card = card
                self.context["current_card"] = card
                break

        # If no card mentioned, use the last card from context
        if not mentioned_card and self.context["current_card"]:
            mentioned_card = self.context["current_card"]

        # Get answer using parent class method
        response = super().get_answer(user_input)
        
        if isinstance(response, dict):
            answer = self.format_response(
                response['answer'],
                intent,
                {"card_name": mentioned_card} if mentioned_card else None
            )
            
            # Update conversation history
            self.conversation_history.append({
                "user": user_input,
                "bot": answer,
                "intent": intent,
                "card": mentioned_card,
                "timestamp": datetime.now()
            })
            
            return answer
        
        return response

    def get_card_by_number(self, number: str) -> str:
        try:
            idx = int(number) - 1
            if 0 <= idx < len(self.available_cards):
                return self.available_cards[idx]
        except ValueError:
            return None
        return None

    def get_card_info(self, card_name: str) -> str:
        """Get basic information about a specific card"""
        # Find card info in training data
        for qa in self.training_data['qa_pairs']:
            if qa['metadata'].get('card_name') == card_name and 'description' in qa['context']:
                return qa['answer']
        return f"Xin lỗi, tôi không tìm thấy thông tin về thẻ {card_name}"

    def update_conversation(self, user_input, response):
        self.conversation_history.append({
            "user": user_input,
            "bot": response
        })
        if len(self.conversation_history) > 5:
            self.conversation_history.pop(0)

    def update_context(self, user_input):
        # Dummy implementation, replace with actual logic
        self.context["last_intent"] = self.get_intent(user_input)
        self.context["questions_asked"].append(user_input)

    def manage_conversation(self, user_input, response):
        # Track conversation state
        self.update_context(user_input)
        
        # Handle multi-turn conversations
        if self.context["last_intent"] == "card_info":
            # Add relevant follow-up responses
            pass
            
        # Save conversation history
        self.conversation_history.append({
            "user": user_input,
            "bot": response,
            "intent": self.context["last_intent"],
            "timestamp": datetime.now()
        })

def test_enhanced_chatbot():
    bot = EnhancedCardBot()
    print("ChatBot đã sẵn sàng! (gõ 'quit' để thoát)")
    print("-" * 50)
    
    while True:
        user_input = input("\nBạn: ")
        if user_input.lower() == 'quit':
            break
            
        response = bot.get_answer(user_input)
        # Print just the answer
        print(f"\nBot: {response}")

if __name__ == "__main__":
    test_enhanced_chatbot()