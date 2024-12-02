import json
from typing import List, Dict
import numpy as np

def generate_qa_pairs(card_data: Dict) -> List[Dict]:
    """Generate question-answer pairs from card data"""
    qa_pairs = []
    
    # Basic card info
    qa_pairs.extend([
        {
            "question": f"Thẻ {card_data['card_name']} là gì?",
            
            "answer": card_data['description'],
            "context": "card_description",
            "metadata": {
                "card_type": card_data.get('card_type', ''),
                "card_name": card_data['card_name']
            }
        },
        {
            "question": f"Có những ưu đãi gì khi dùng thẻ {card_data['card_name']}?",
            "answer": " ".join(card_data.get('features', {}).get('gifts', [])),
            "context": "card_benefits",
            "metadata": {
                "card_type": card_data.get('card_type', ''),
                "card_name": card_data['card_name']
            }
        }
    ])

    # Benefits and features
    benefits = card_data.get('features', {}).get('benefits', [])
    if benefits:
        qa_pairs.append({
            "question": f"Quyền lợi và tính năng của thẻ {card_data['card_name']} là gì?",
            "variations": [
                f"Lợi ích thẻ {card_data['card_name']}",
                f"Thông tin thẻ {card_data['card_name']}",
                f"Giới thiệu thẻ {card_data['card_name']}"
            ],
            "answer": "\n".join(f"- {benefit}" for benefit in benefits),
            "context": "card_features",
            "metadata": {
                "card_type": card_data.get('card_type', ''),
                "card_name": card_data['card_name']
            }
        })

    # Terms and conditions
    conditions = card_data.get('terms_and_conditions', {})
    if conditions.get('conditions'):
        qa_pairs.append({
            "question": f"Điều kiện mở thẻ {card_data['card_name']} là gì?",
            "answer": conditions['conditions'],
            "context": "card_conditions",
            "metadata": {
                "card_type": card_data.get('card_type', ''),
                "card_name": card_data['card_name']
            }
        })

    if conditions.get('fees'):
        qa_pairs.append({
            "question": f"Phí và lãi suất của thẻ {card_data['card_name']} là bao nhiêu?",
            "answer": conditions['fees'],
            "context": "card_fees",
            "metadata": {
                "card_type": card_data.get('card_type', ''),
                "card_name": card_data['card_name']
            }
        })

    # FAQs
    for question, answer in card_data.get('faqs', {}).items():
        qa_pairs.append({
            "question": question,
            "answer": answer,
            "context": "card_faqs",
            "metadata": {
                "card_type": card_data.get('card_type', ''),
                "card_name": card_data['card_name']
            }
        })

    return qa_pairs

def generate_greeting_qa_pairs():
    """Generate greeting and farewell training data"""
    qa_pairs = []
    
    responses = {
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

    # Generate greeting QA pairs
    greeting_patterns = [
        "xin chào", "chào", "hi", "hello", "hey",
        "chào buổi sáng", "chào buổi chiều", "chào buổi tối"
    ]
    
    for pattern in greeting_patterns:
        qa_pairs.append({
            "question": pattern,
            "answer": np.random.choice(responses["greeting"]),
            "context": "greeting",
            "metadata": {"type": "greeting"}
        })

    # Generate farewell QA pairs  
    farewell_patterns = [
        "tạm biệt", "goodbye", "bye", "bái bai",
        "cảm ơn", "thanks", "thank you"
    ]

    for pattern in farewell_patterns:
        qa_pairs.append({
            "question": pattern, 
            "answer": np.random.choice(responses["farewell"]),
            "context": "farewell",
            "metadata": {"type": "farewell"}
        })

    return qa_pairs

def enhance_answer(answer: str, context: str) -> str:
    """Add natural language elements to answers"""
    prefixes = {
        "card_description": [
            "Để giải thích về thẻ này, ",
            "Tôi xin được chia sẻ rằng ",
            "Thẻ này có đặc điểm là "
        ],
        "card_benefits": [
            "Khi sử dụng thẻ này, bạn sẽ được ",
            "Thẻ mang đến cho bạn những ưu đãi sau: ",
            "Quyền lợi của chủ thẻ bao gồm "
        ],
        "card_conditions": [
            "Để đăng ký thẻ này, bạn cần đáp ứng: ",
            "Điều kiện phát hành thẻ bao gồm: ",
            "Yêu cầu cần có để mở thẻ là "
        ],
        "card_fees": [
            "Về phí và lãi suất, ",
            "Chi phí sử dụng thẻ bao gồm: ",
            "Thông tin về phí như sau: "
        ]
    }
    
    if context in prefixes:
        prefix = np.random.choice(prefixes[context])
        return f"{prefix}{answer}"
    return answer

def generate_variations(question: str) -> List[str]:
    """Generate more natural variations of questions"""
    variations = []
    variations.append(question)
    
    # Enhanced replacements
    replacements = {
        "là gì": ["như thế nào", "ra sao", "là như thế nào", "có thể giới thiệu về"],
        "có những": ["có các", "có những loại", "có các loại", "bao gồm những"],
        "bao nhiêu": ["là bao nhiêu", "là mấy", "mấy", "khoảng bao nhiêu"],
        "điều kiện": ["yêu cầu", "cần những gì", "cần đáp ứng điều kiện gì"],
        "cho tôi biết": ["vui lòng cho biết", "xin hỏi", "làm ơn cho biết"],
        "muốn hỏi": ["có thể cho tôi biết", "tôi muốn tìm hiểu về"]
    }
    
    # Add politeness variations
    polite_prefixes = ["xin hỏi", "làm ơn cho", "vui lòng", "cho tôi hỏi"]
    
    # Generate basic variations
    for old, new_list in replacements.items():
        if old in question.lower():
            for new in new_list:
                variations.append(question.lower().replace(old, new))
    
    # Add polite variations
    base_variations = variations.copy()
    for variant in base_variations:
        for prefix in polite_prefixes:
            if not any(p in variant.lower() for p in polite_prefixes):
                variations.append(f"{prefix} {variant}")
    
    return list(set(variations))

def create_training_data():
    # Load scraped data
    with open('training_card_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_qa_pairs = []
    
    # Add greeting QA pairs first
    all_qa_pairs.extend(generate_greeting_qa_pairs())
    
    # Process each card
    for card in data['cards_data']:
        card_info = {
            'card_name': card['metadata']['card_name'],
            'card_type': card['metadata']['card_type'],
            'description': card.get('description', ''),
            'features': {
                'benefits': card.get('features', {}).get('benefits', []),
                'gifts': card.get('features', {}).get('gifts', []),
                'privileges': card.get('features', {}).get('privileges', [])
            },
            'terms_and_conditions': {
                'conditions': card.get('terms_and_conditions', {}).get('conditions', ''),
                'fees': card.get('terms_and_conditions', {}).get('fees', ''),
                'documents': card.get('terms_and_conditions', {}).get('documents', '')
            },
            'faqs': card.get('faqs', {})
        }
        
        # Get base QA pairs for this card
        card_qa_pairs = generate_qa_pairs(card_info)
        
        # Generate variations and enhance answers
        for qa in card_qa_pairs:
            base_question = qa['question']
            question_variations = generate_variations(base_question)
            enhanced_answer = enhance_answer(qa['answer'], qa['context'])
            
            # Add each variation as a separate QA pair
            for variant in question_variations:
                all_qa_pairs.append({
                    "question": variant,
                    "answer": enhanced_answer,
                    "context": qa['context'],
                    "metadata": qa['metadata']
                })
            
            # If there are specific variations in the QA pair, add those too
            if 'variations' in qa:
                for variant in qa['variations']:
                    all_qa_pairs.append({
                        "question": variant,
                        "answer": enhanced_answer,
                        "context": qa['context'],
                        "metadata": qa['metadata']
                    })
    
    # Create final training data structure
    training_data = {
        "dataset_info": {
            "name": "HDBank Cards QA Dataset",
            "version": "1.0",
            "description": "Question-Answer pairs about HDBank credit cards",
            "language": "vi",
            "total_qa_pairs": len(all_qa_pairs)
        },
        "qa_pairs": all_qa_pairs
    }
    
    # Save training data
    with open('training_data.json', 'w', encoding='utf-8') as f:
        json.dump(training_data, f, ensure_ascii=False, indent=4)
    
    print(f"Generated {len(all_qa_pairs)} QA pairs for training")

if __name__ == "__main__":
    create_training_data()