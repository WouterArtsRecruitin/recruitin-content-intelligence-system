"""
ICP SCORING CALCULATOR - ZAPIER CODE BY ZAPIER STEP
Voor: Recruitin B.V. - Pipedrive ICP automation
"""

def calculate_icp_score(input_data):
    """
    Berekent ICP score op basis van 7 criteria
    
    Args:
        input_data (dict): Pipedrive deal fields
        
    Returns:
        dict: {'icp_score': float, 'icp_match': str, 'breakdown': dict}
    """
    
    # ========================================
    # 1. BEDRIJFSGROOTTE (Weight: 2x)
    # ========================================
    bedrijfsgrootte = input_data.get('bedrijfsgrootte_fte', 0)
    
    if bedrijfsgrootte < 50:
        score_grootte = 0
    elif 50 <= bedrijfsgrootte < 200:
        score_grootte = 1
    elif 200 <= bedrijfsgrootte <= 800:
        score_grootte = 2
    else:  # > 800
        score_grootte = 3
    
    weighted_grootte = score_grootte * 2.0
    
    # ========================================
    # 2. SECTOR (Weight: 1.5x)
    # ========================================
    sector = input_data.get('icp_sector', '').lower()
    
    perfect_sectors = ['oil & gas', 'renewable energy', 'wind energy']
    target_sectors = ['productie', 'constructie', 'automation', 'engineering']
    adjacent_sectors = ['it', 'engineering services', 'technical services']
    
    if any(s in sector for s in perfect_sectors):
        score_sector = 3
    elif any(s in sector for s in target_sectors):
        score_sector = 2
    elif any(s in sector for s in adjacent_sectors):
        score_sector = 1
    else:
        score_sector = 0
    
    weighted_sector = score_sector * 1.5
    
    # ========================================
    # 3. REGIO (Weight: 1x)
    # ========================================
    regio = input_data.get('icp_regio', '').lower()
    
    target_regio = ['gelderland', 'overijssel', 'noord-brabant']
    
    # Check for multiple locations in target area
    regio_count = sum(1 for r in target_regio if r in regio)
    
    if regio_count >= 2:
        score_regio = 3  # Multi-locatie
    elif regio_count == 1:
        score_regio = 2  # Target regio
    elif regio == 'nederland' or any(prov in regio for prov in ['utrecht', 'zuid-holland', 'noord-holland']):
        score_regio = 1  # Andere NL provincie
    else:
        score_regio = 0  # Buiten NL
    
    weighted_regio = score_regio * 1.0
    
    # ========================================
    # 4. RECRUITMENT TYPE (Weight: 1.5x)
    # ========================================
    recruitment_type = input_data.get('recruitment_type', '').lower()
    
    if 'rpo' in recruitment_type:
        score_type = 3
    elif any(t in recruitment_type for t in ['w&s', 'werving & selectie', 'interim']):
        score_type = 2
    elif 'recruitment marketing' in recruitment_type:
        score_type = 1
    else:
        score_type = 0
    
    weighted_type = score_type * 1.5
    
    # ========================================
    # 5. BUDGET RANGE (Weight: 2x)
    # ========================================
    budget_range = input_data.get('budget_range', '').lower()
    
    # Extract number from budget string (e.g., "€50k-€100k" -> 75)
    if '100' in budget_range or '€100k' in budget_range:
        score_budget = 3
    elif '50' in budget_range and '100' in budget_range:
        score_budget = 2
    elif '25' in budget_range or '50' in budget_range:
        score_budget = 1
    else:
        score_budget = 0
    
    weighted_budget = score_budget * 2.0
    
    # ========================================
    # 6. DECISION MAKER (Weight: 1x)
    # ========================================
    decision_maker = input_data.get('decision_maker_role', '').lower()
    
    if any(role in decision_maker for role in ['ceo', 'cfo', 'coo', 'hr director', 'directeur']):
        score_dm = 3
    elif any(role in decision_maker for role in ['manager', 'head of']):
        score_dm = 2
    elif any(role in decision_maker for role in ['coordinator', 'specialist', 'officer']):
        score_dm = 1
    else:
        score_dm = 0
    
    weighted_dm = score_dm * 1.0
    
    # ========================================
    # 7. URGENTIE (Weight: 0.5x)
    # ========================================
    urgentie = input_data.get('urgentie', '').lower()
    
    if 'urgent' in urgentie or '< 1' in urgentie:
        score_urgentie = 3
    elif 'normaal' in urgentie or '1-3' in urgentie:
        score_urgentie = 2
    elif 'langzaam' in urgentie or '> 3' in urgentie:
        score_urgentie = 1
    else:
        score_urgentie = 0
    
    weighted_urgentie = score_urgentie * 0.5
    
    # ========================================
    # TOTAL SCORE CALCULATION
    # ========================================
    total_score = (
        weighted_grootte +
        weighted_sector +
        weighted_regio +
        weighted_type +
        weighted_budget +
        weighted_dm +
        weighted_urgentie
    )
    
    # Max possible score: 28.5
    # ICP threshold: 14.25 (50%)
    icp_match = "Yes" if total_score >= 14.25 else "No"
    
    # Breakdown for debugging
    breakdown = {
        'bedrijfsgrootte': f"{score_grootte}/3 (weighted: {weighted_grootte}/6)",
        'sector': f"{score_sector}/3 (weighted: {weighted_sector}/4.5)",
        'regio': f"{score_regio}/3 (weighted: {weighted_regio}/3)",
        'recruitment_type': f"{score_type}/3 (weighted: {weighted_type}/4.5)",
        'budget': f"{score_budget}/3 (weighted: {weighted_budget}/6)",
        'decision_maker': f"{score_dm}/3 (weighted: {weighted_dm}/3)",
        'urgentie': f"{score_urgentie}/3 (weighted: {weighted_urgentie}/1.5)"
    }
    
    return {
        'icp_score': round(total_score, 2),
        'icp_match': icp_match,
        'score_percentage': round((total_score / 28.5) * 100, 1),
        'breakdown': breakdown
    }


# ========================================
# ZAPIER INTERFACE
# ========================================
# In Zapier "Code by Zapier" step, use this:

# Input data komt van vorige Zapier stap
input_data = {
    'bedrijfsgrootte_fte': int(input.get('bedrijfsgrootte_fte', 0)),
    'icp_sector': input.get('icp_sector', ''),
    'icp_regio': input.get('icp_regio', ''),
    'recruitment_type': input.get('recruitment_type', ''),
    'budget_range': input.get('budget_range', ''),
    'decision_maker_role': input.get('decision_maker_role', ''),
    'urgentie': input.get('urgentie', '')
}

# Calculate
result = calculate_icp_score(input_data)

# Output voor volgende Zapier stap
output = {
    'icp_score': result['icp_score'],
    'icp_match': result['icp_match'],
    'score_percentage': result['score_percentage'],
    'breakdown_text': '\n'.join([f"{k}: {v}" for k, v in result['breakdown'].items()])
}
