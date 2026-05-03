"""
Prompt Templates for Civic Twin Navigator.

All AI prompts are centralized here for:
- Maintainability
- Consistency
- Easy updates
- Separation of concerns
"""


# ─────────────────────────────────────────────
# SYSTEM INSTRUCTIONS
# ─────────────────────────────────────────────

INTENT_CONTEXT_SYSTEM = """
You are the Intent & Context Agent for Civic Twin Navigator.
Your job is to understand user inputs about elections and voting.

Rules:
- Be neutral, never promote any political party or candidate
- Be helpful and empathetic especially to first-time voters
- Extract only factual information from user input
- Always respond in valid JSON format when asked
- Identify user concerns and knowledge gaps
- Respect all languages and literacy levels
"""

POLICY_RETRIEVAL_SYSTEM = """
You are the Policy Retrieval Agent for Civic Twin Navigator.
You provide accurate, unbiased information about Indian election procedures.

Rules:
- Only provide factual, verified election information
- Reference Election Commission of India guidelines
- Never promote any political party or candidate
- Be precise about legal requirements
- Clearly state when information may vary by state
- Always mention source as Election Commission of India
- If unsure, say so and recommend official ECI website
- Always return valid JSON with no trailing commas
- Use double quotes for all strings in JSON
"""

CONSISTENCY_VERIFICATION_SYSTEM = """
You are the Consistency & Verification Agent for Civic Twin Navigator.
Your job is to validate and verify election related information.

Rules:
- Be thorough and precise in verification
- Flag any inconsistencies clearly
- Suggest corrections when issues are found
- Never approve invalid or contradictory information
- Always return valid JSON with no trailing commas
- Use double quotes for all strings in JSON
- Be helpful not alarming when flagging issues
"""

JOURNEY_PLANNER_SYSTEM = """
You are the Journey Planner Agent for Civic Twin Navigator.
You create personalized election participation journeys for Indian voters.

Rules:
- Create realistic and achievable step by step journeys
- Personalize based on user profile and situation
- Include clear deadlines and timeframes
- Make steps actionable and specific
- Remove steps not relevant to user situation
- Always return valid JSON with no trailing commas
- Use double quotes for all strings in JSON
"""

SIMULATION_SYSTEM = """
You are the Simulation Agent for Civic Twin Navigator.
You create interactive learning scenarios for Indian voters.

Rules:
- Create realistic and educational scenarios
- Make scenarios relevant to Indian election context
- Be encouraging and supportive in responses
- Never use political party names or real candidates
- Make learning engaging and practical
- Always return valid JSON with no trailing commas
- Use double quotes for all strings in JSON
"""

ASSESSMENT_SYSTEM = """
You are the Assessment Agent for Civic Twin Navigator.
You evaluate voter readiness and provide explainable scores.

Rules:
- Use 0-100 scale for all scores
- Explain each sub-score with reasoning
- Base scores on user profile, completed steps, and documents
- Be encouraging but honest
- Always return valid JSON with no trailing commas
"""

PREDICTION_SYSTEM = """
You are the Prediction Agent for Civic Twin Navigator.
You analyze user profiles to predict potential election participation failures.

Rules:
- Base predictions on common patterns for Indian voters
- Never assume based on demographics
- Be helpful, not alarming
- Focus on actionable prevention
- Always return valid JSON with no trailing commas
"""

ACCESSIBILITY_SYSTEM = """
You are the Accessibility Agent for Civic Twin Navigator.
You make election information accessible to all Indian voters.

Rules:
- Use simple words and short sentences
- Translate to user's preferred language
- Adapt for different literacy levels
- Be patient and encouraging
- Respect all users regardless of background
"""

SAFETY_SYSTEM = """
You are the Safety Agent for Civic Twin Navigator.
Your ONLY role is to ensure election information is accurate, neutral, and safe.

Rules (strict):
- Never promote any political party, candidate, ideology, or movement.
- Never provide instructions that could manipulate voter behavior.
- Flag any misinformation about voter eligibility, registration, deadlines, documents, or polling.
- Be precise, factual, and non-prescriptive.
- Always return valid JSON with no trailing commas and double-quoted strings.
- If uncertain, mark risk_level as medium or high and provide clear reasons.
"""


# ─────────────────────────────────────────────
# INTENT & CONTEXT AGENT PROMPTS
# ─────────────────────────────────────────────

def get_analyze_intent_prompt(user_input: str, profile_context: str = "") -> str:
    """Prompt for analyzing user intent and extracting context."""
    return f"""
Analyze this user input about elections/voting and extract information.

User Input: "{user_input}"

{profile_context}

Extract and return JSON with this exact structure:
{{
    "intent": "one of: registration_query, eligibility_query, document_query, timeline_query, polling_query, general_query, scenario_query, help_request",
    "extracted_info": {{
        "location": "city or area mentioned or null",
        "age": "age if mentioned or null",
        "voter_status": "one of: first_time, registered, unsure or null",
        "occupation": "student/worker/etc or null",
        "residence_type": "hostel/rented/owned/etc or null",
        "language_preference": "detected language code like en/hi/mr or en",
        "literacy_level": "one of: basic/intermediate/advanced based on writing style",
        "special_needs": "any accessibility needs mentioned or null"
    }},
    "concerns": ["list", "of", "specific", "concerns", "mentioned"],
    "knowledge_gaps": ["things", "user", "seems", "unsure", "about"],
    "confidence_level": "one of: low/medium/high - how confident user seems",
    "requires_clarification": true or false,
    "clarification_questions": ["question if clarification needed or empty list"],
    "summary": "one sentence summary of what user needs"
}}
"""


def get_build_profile_prompt(user_input: str, session_id: str, timestamp: str) -> str:
    """Prompt for building a Civic Twin profile."""
    return f"""
Based on this user input, create a complete Civic Twin profile for an
Indian election assistance system.

User Input: "{user_input}"

Create a detailed profile with this exact JSON structure:
{{
    "session_id": "{session_id}",
    "personal_info": {{
        "location": "extracted city/area or Not specified",
        "state": "extracted Indian state or Not specified",
        "age": null or number,
        "occupation": "extracted or Not specified",
        "residence_type": "hostel/rented/owned/parents_home or Not specified"
    }},
    "voter_profile": {{
        "voter_status": "first_time/registered/unsure",
        "is_eligible": true or false or null,
        "registration_status": "registered/not_registered/unknown",
        "has_voter_id": true or false or null,
        "constituency": "if mentioned or null"
    }},
    "document_status": {{
        "has_aadhar": null,
        "has_address_proof": null,
        "has_age_proof": null,
        "document_concerns": ["list of document concerns mentioned"]
    }},
    "accessibility_profile": {{
        "language_preference": "language code like en/hi/mr",
        "literacy_level": "basic/intermediate/advanced",
        "needs_voice_support": false,
        "needs_simple_language": false,
        "special_needs": null
    }},
    "risk_factors": ["list", "of", "identified", "risk", "factors"],
    "priority_concerns": ["most", "urgent", "concerns", "to", "address"],
    "created_at": "{timestamp}",
    "profile_completeness": 0
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas.
"""


def get_clarification_prompt(missing_info: list) -> str:
    """Prompt for generating clarification questions."""
    return f"""
Generate friendly, simple questions to collect missing voter information.

Missing information needed: {missing_info}

Rules:
- Ask maximum 2 questions at a time
- Use simple conversational language
- Be encouraging and friendly
- Frame questions in context of helping them vote

Return JSON:
{{
    "questions": ["question 1", "question 2"],
    "friendly_message": "encouraging message to motivate user",
    "why_needed": "brief explanation of why this info helps"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas.
"""


# ─────────────────────────────────────────────
# POLICY RETRIEVAL AGENT PROMPTS
# ─────────────────────────────────────────────

def get_eligibility_prompt(profile_context: str = "") -> str:
    """Prompt for getting voter eligibility rules."""
    return f"""
Provide voter eligibility rules for India.
{profile_context}

Return this exact JSON structure:
{{
  "eligibility_criteria": {{
    "minimum_age": 18,
    "citizenship_required": true,
    "residence_requirement": "Must be ordinarily resident in the constituency",
    "disqualifications": ["Declared of unsound mind", "Corrupt practices conviction", "Criminal sentence over 2 years"]
  }},
  "user_eligibility": {{
    "is_eligible": true,
    "eligibility_reason": "User meets basic eligibility criteria",
    "age_check": "passed",
    "concerns": []
  }},
  "next_steps": ["Check your name on electoral roll at voters.eci.gov.in", "Register if not already registered using Form 6"],
  "official_source": "Election Commission of India - eci.gov.in",
  "important_notes": ["Eligibility is checked at constituency level", "Registration deadline varies by election"]
}}

IMPORTANT: Return only valid JSON. No markdown. No extra text. No trailing commas.
"""


def get_registration_prompt(voter_status: str, location: str) -> str:
    """Prompt for getting voter registration process."""
    return f"""
Provide voter registration process for India.
User type: {voter_status}
Location: {location}

Return this exact JSON:
{{
  "registration_method": {{
    "online": {{
      "platform": "voters.eci.gov.in or Voter Helpline App",
      "form": "Form 6 for new voters",
      "steps": [
        "Visit voters.eci.gov.in",
        "Click on Register as New Voter",
        "Fill Form 6 with personal details",
        "Upload required documents",
        "Submit and note application number"
      ]
    }},
    "offline": {{
      "location": "Booth Level Officer or Electoral Registration Office",
      "form": "Form 6",
      "steps": [
        "Visit nearest Electoral Registration Office",
        "Collect and fill Form 6",
        "Attach required documents",
        "Submit to Booth Level Officer"
      ]
    }}
  }},
  "required_documents": {{
    "mandatory": ["Age Proof", "Address Proof", "Photograph"],
    "age_proof_options": ["Birth Certificate", "School Certificate", "Passport", "PAN Card"],
    "address_proof_options": ["Aadhar Card", "Passport", "Bank Passbook", "Utility Bill"],
    "photo_requirement": "Recent passport size photograph"
  }},
  "timeline": {{
    "processing_time": "15 to 30 days",
    "verification_process": "Field verification by Booth Level Officer",
    "confirmation_method": "SMS and email notification"
  }},
  "special_cases": {{
    "hostel_students": "Use hostel certificate from warden as address proof",
    "migrants": "Can register at current place of residence",
    "no_fixed_address": "Contact Electoral Registration Officer for assistance"
  }},
  "important_deadlines": ["Check ECI website for current deadlines"],
  "helpline": "1950",
  "official_website": "voters.eci.gov.in"
}}

IMPORTANT: Return only valid JSON. No markdown. No extra text. No trailing commas.
"""


def get_document_requirements_prompt(profile_context: str = "") -> str:
    """Prompt for getting document requirements."""
    return f"""
Provide voter registration document requirements for India.
{profile_context}

Return this exact JSON structure with no trailing commas:
{{
  "mandatory_documents": [
    {{
      "type": "Age Proof",
      "options": ["Birth Certificate", "School Leaving Certificate", "Passport", "PAN Card", "Driving License"],
      "notes": "Any one document showing date of birth"
    }},
    {{
      "type": "Address Proof",
      "options": ["Aadhar Card", "Passport", "Driving License", "Bank Passbook", "Utility Bill", "Rent Agreement"],
      "notes": "Any one document showing current address"
    }},
    {{
      "type": "Photograph",
      "options": ["Recent Passport Size Photo"],
      "notes": "Color photo with white background preferred"
    }}
  ],
  "special_situations": {{
    "hostel_students": "Hostel Certificate from Warden on institute letterhead",
    "no_aadhar": "Use Passport, Driving License or Bank Passbook instead",
    "no_fixed_address": "Contact local Electoral Registration Officer",
    "parents_home": "Use parent address proof with relationship proof"
  }},
  "document_tips": [
    "Keep original documents for verification",
    "Ensure documents are valid and not expired",
    "Use clear scanned copies for online application"
  ],
  "common_mistakes": [
    "Using expired documents",
    "Address mismatch between documents",
    "Submitting unclear photocopies"
  ],
  "where_to_get_docs": {{
    "aadhar": "Visit uidai.gov.in or nearest Aadhar enrollment center",
    "birth_certificate": "Municipal Corporation of your birth place",
    "other": "Contact Electoral Registration Office for guidance"
  }}
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


def get_poll_day_prompt() -> str:
    """Prompt for getting poll day guidance."""
    return """
Provide complete poll day guidance for Indian voters.

Return this exact JSON:
{
  "before_poll_day": {
    "check_name_on_list": "Visit voters.eci.gov.in or call 1950 to verify your name",
    "find_polling_station": "Check your Voter ID card or voters.eci.gov.in for booth details",
    "what_to_prepare": ["Carry any one valid photo ID", "Note your booth number and address", "Check polling hours"]
  },
  "valid_id_proofs": [
    "Voter ID Card (EPIC)",
    "Aadhar Card",
    "Passport",
    "Driving License",
    "PAN Card",
    "MNREGA Job Card",
    "Bank or Post Office Passbook with photo",
    "Pension document with photo",
    "Service Identity Card with photo"
  ],
  "at_polling_station": {
    "process_steps": [
      "Join the queue at your designated polling booth",
      "Show your photo ID to polling officer",
      "Get your finger marked with indelible ink",
      "Press the button on EVM for your choice",
      "Verify on VVPAT slip"
    ],
    "voting_machine": "Electronic Voting Machine press button next to candidate name",
    "vvpat": "Voter Verified Paper Audit Trail shows slip for 7 seconds to verify",
    "time_required": "Approximately 5 to 10 minutes"
  },
  "polling_hours": "7:00 AM to 6:00 PM general timing may vary by constituency",
  "rights_at_booth": [
    "Right to vote without being pressured",
    "Right to cast NOTA vote",
    "Right to complain if facing issues"
  ],
  "what_not_to_do": [
    "Do not carry mobile phones inside voting compartment",
    "Do not take photos of your vote",
    "Do not campaign within 100 meters of booth"
  ],
  "if_name_missing": "Contact Presiding Officer or call 1950 helpline immediately",
  "helpline": "1950"
}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


def get_specific_query_prompt(query: str, profile_context: str = "") -> str:
    """Prompt for answering specific election queries."""
    return f"""
Answer this election question accurately and completely.

Question: "{query}"
{profile_context}

Provide a thorough and complete answer covering all aspects of the question.

Return this exact JSON:
{{
  "question": "{query}",
  "answer": "Write a complete and detailed answer here. Cover all aspects. Do not cut short. Minimum 3 to 4 sentences.",
  "key_points": [
    "Complete key point 1 with full detail",
    "Complete key point 2 with full detail",
    "Complete key point 3 with full detail"
  ],
  "action_required": true,
  "action_steps": [
    "Step 1 with full instruction",
    "Step 2 with full instruction",
    "Step 3 with full instruction"
  ],
  "confidence_level": "high",
  "official_source": "Election Commission of India - eci.gov.in",
  "disclaimer": "Information based on ECI guidelines. Always verify at eci.gov.in for latest updates."
}}

IMPORTANT:
- Return only valid JSON
- No markdown
- No trailing commas
- Answer field must be complete and not cut short
- All fields must have complete values
"""


# ─────────────────────────────────────────────
# JOURNEY PLANNER AGENT PROMPTS
# ─────────────────────────────────────────────

def get_journey_prompt(session_id: str, voter_status: str, location: str,
                       occupation: str, residence: str, risk_factors: list,
                       doc_status: dict, timestamp: str) -> str:
    """Prompt for creating a personalized election journey."""
    return f"""
Create a personalized election participation journey for this Indian voter.

User Profile:
- Voter Status: {voter_status}
- Location: {location}
- Occupation: {occupation}
- Residence Type: {residence}
- Risk Factors: {risk_factors}
- Document Status: {doc_status}

Create a journey with 5 phases. Each phase has specific steps.
Make it personalized based on their situation.

Return this exact JSON:
{{
  "session_id": "{session_id}",
  "journey_title": "Your Personal Voter Registration Journey",
  "total_phases": 5,
  "estimated_completion_days": 30,
  "phases": [
    {{
      "phase_id": "phase_1",
      "phase_number": 1,
      "title": "Eligibility Verification",
      "description": "Confirm you are eligible to vote",
      "status": "pending",
      "estimated_days": 1,
      "steps": [
        {{
          "step_id": "step_1_1",
          "title": "Check your age eligibility",
          "description": "Confirm you are 18 years or older",
          "action": "Verify your date of birth against voter eligibility requirements",
          "is_completed": false,
          "is_required": true,
          "resources": ["voters.eci.gov.in"]
        }}
      ]
    }}
  ],
  "personalization_notes": ["Journey customized based on your profile"],
  "important_reminders": ["Check registration deadline for your constituency"],
  "created_at": "{timestamp}"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
Create all 5 phases with relevant steps for this voter profile.
"""


# ─────────────────────────────────────────────
# SIMULATION AGENT PROMPTS
# ─────────────────────────────────────────────

def get_mission_prompt(mission_number: int, topic: str,
                       location: str, voter_status: str) -> str:
    """Prompt for generating an interactive mission."""
    return f"""
Create Mission {mission_number} for an Indian voter learning system.

Mission Topic: {topic}
User Location: {location}
User Voter Status: {voter_status}

Create an engaging interactive mission with scenarios and questions.

Return this exact JSON:
{{
  "mission_id": "mission_{mission_number}",
  "mission_number": {mission_number},
  "title": "Mission {mission_number}: {topic}",
  "description": "What this mission covers",
  "learning_objectives": ["Objective 1", "Objective 2", "Objective 3"],
  "estimated_time_minutes": 10,
  "scenario": {{
    "story": "Engaging scenario story relevant to this mission topic in 2 to 3 sentences",
    "context": "Additional context for the scenario",
    "character": "Priya, a 20-year-old student in {location}"
  }},
  "questions": [
    {{
      "question_id": "q1",
      "question": "First question about {topic}",
      "type": "multiple_choice",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A",
      "explanation": "Why this is correct with full explanation",
      "hint": "Helpful hint if stuck"
    }},
    {{
      "question_id": "q2",
      "question": "Second question about {topic}",
      "type": "true_false",
      "options": ["True", "False"],
      "correct_answer": "True",
      "explanation": "Why this is correct with full explanation",
      "hint": "Helpful hint if stuck"
    }},
    {{
      "question_id": "q3",
      "question": "Third practical question about {topic}",
      "type": "multiple_choice",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option B",
      "explanation": "Why this is correct with full explanation",
      "hint": "Helpful hint if stuck"
    }}
  ],
  "key_takeaways": ["Key learning 1", "Key learning 2", "Key learning 3"],
  "completion_message": "Encouraging message on mission completion",
  "next_mission_preview": "Brief preview of next mission"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
Make questions specific to Indian election process. Do not mention real political parties.
"""


def get_scenario_prompt(scenario: str, location: str) -> str:
    """Prompt for running a what-if scenario simulation."""
    return f"""
Simulate this what-if scenario for an Indian voter in {location}.

Scenario: "{scenario}"

Provide realistic outcomes and practical solutions based on
Election Commission of India guidelines.

Return this exact JSON:
{{
  "scenario": "{scenario}",
  "scenario_type": "type of scenario like missed_deadline or document_issue",
  "is_recoverable": true,
  "immediate_impact": "What happens immediately in this scenario",
  "outcomes": [
    {{
      "outcome": "Most likely outcome",
      "probability": "high",
      "description": "Detailed description of this outcome"
    }}
  ],
  "recovery_steps": [
    {{
      "step": 1,
      "action": "First action to take",
      "timeframe": "immediately",
      "contact": "who to contact if needed"
    }},
    {{
      "step": 2,
      "action": "Second action to take",
      "timeframe": "within 24 hours",
      "contact": "relevant authority"
    }}
  ],
  "prevention_tips": [
    "How to prevent this in future",
    "Early warning signs to watch for"
  ],
  "helpline": "1950",
  "official_resource": "voters.eci.gov.in",
  "confidence_level": "high",
  "disclaimer": "Based on ECI guidelines. Specific cases may vary."
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


def get_poll_day_simulation_prompt(location: str) -> str:
    """Prompt for simulating the complete poll day experience."""
    return f"""
Create an interactive poll day simulation for a voter in {location}, India.

Make it realistic and educational.

Return this exact JSON:
{{
  "simulation_title": "Your Poll Day Experience Simulation",
  "location": "{location}",
  "timeline": [
    {{
      "time": "6:30 AM",
      "event": "Wake up and preparation",
      "action": "Check your voter ID and polling booth address",
      "tip": "Keep your ID ready the night before"
    }},
    {{
      "time": "7:00 AM",
      "event": "Polling booths open",
      "action": "You can go vote from this time",
      "tip": "Morning hours are usually less crowded"
    }},
    {{
      "time": "8:00 AM",
      "event": "Arrive at polling booth",
      "action": "Find your queue based on your voter ID number",
      "tip": "Check your queue number on your voter slip"
    }},
    {{
      "time": "8:20 AM",
      "event": "Voting",
      "action": "Press the button on EVM next to your chosen candidate",
      "tip": "Take your time, no one can see your vote"
    }},
    {{
      "time": "8:27 AM",
      "event": "Done",
      "action": "Exit the booth, your vote has been cast",
      "tip": "You can wear your ink mark with pride"
    }}
  ],
  "possible_disruptions": [
    {{
      "situation": "Your name is not found on the list",
      "solution": "Contact the Presiding Officer and call 1950 helpline"
    }},
    {{
      "situation": "You forgot your voter ID",
      "solution": "Any 9 alternative photo IDs are accepted including Aadhar Card"
    }}
  ],
  "dos": [
    "Carry your voter ID or valid alternate photo ID",
    "Arrive early to avoid long queues"
  ],
  "donts": [
    "Do not carry mobile phone inside voting compartment",
    "Do not take photos of your vote"
  ],
  "emergency_contact": "1950 voter helpline"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


def get_check_answer_prompt(question_id: str, user_answer: str,
                            correct_answer: str, is_correct: bool,
                            explanation: str) -> str:
    """Prompt for checking and giving feedback on mission answers."""
    points = "10" if is_correct else "0"
    return f"""
Provide encouraging feedback for this quiz answer.

Question ID: {question_id}
User Answer: "{user_answer}"
Correct Answer: "{correct_answer}"
Is Correct: {is_correct}
Explanation: "{explanation}"

Return this exact JSON:
{{
  "question_id": "{question_id}",
  "is_correct": {str(is_correct).lower()},
  "user_answer": "{user_answer}",
  "correct_answer": "{correct_answer}",
  "feedback_message": "encouraging feedback message",
  "explanation": "{explanation}",
  "points_earned": {points},
  "encouragement": "motivational message for the user"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


# ─────────────────────────────────────────────
# ASSESSMENT AGENT PROMPTS
# ─────────────────────────────────────────────

def get_readiness_score_prompt(session_id: str, age: any, location: str,
                               voter_status: str, has_aadhar: any,
                               document_concerns: list, completed_steps: int,
                               total_steps: int, profile_completeness: int,
                               timestamp: str) -> str:
    """Prompt for calculating voter readiness score."""
    return f"""
Calculate overall voter readiness score for this Indian voter.

User Profile:
- Age: {age}
- Location: {location}
- Voter Status: {voter_status}
- Has Aadhar: {has_aadhar}
- Document Concerns: {document_concerns}

Journey Progress:
- Steps Completed: {completed_steps} / {total_steps}
- Profile Completeness: {profile_completeness}%

Return this exact JSON:
{{
  "session_id": "{session_id}",
  "overall_score": 65,
  "scores": {{
    "legal_readiness": {{
      "score": 85,
      "explanation": "User meets age and citizenship requirements. No legal barriers detected.",
      "max_score": 100,
      "status": "good"
    }},
    "document_readiness": {{
      "score": 50,
      "explanation": "Has age proof and Aadhar but missing clear address proof for hostel.",
      "max_score": 100,
      "status": "needs_attention"
    }},
    "timeline_readiness": {{
      "score": 35,
      "explanation": "Journey just started. No registration steps completed yet.",
      "max_score": 100,
      "status": "needs_improvement"
    }},
    "poll_day_readiness": {{
      "score": 20,
      "explanation": "Not yet registered. Poll day preparation cannot begin until registration is confirmed.",
      "max_score": 100,
      "status": "early_stage"
    }}
  }},
  "overall_status": "needs_improvement",
  "key_improvement_areas": ["Arrange address proof", "Complete registration"],
  "quick_wins": ["Age proof already available", "Aadhar card ready"],
  "improvement_tips": ["Start with document collection", "Use Voter Helpline App"],
  "generated_at": "{timestamp}"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


def get_proof_of_readiness_prompt(session_id: str, profile: dict,
                                  journey: dict, score: dict,
                                  timestamp: str) -> str:
    """Prompt for generating proof of readiness certificate."""
    return f"""
Generate a Proof of Readiness summary for this voter.

Session: {session_id}
Profile: {profile}
Journey: {journey}
Score: {score}

Return this exact JSON:
{{
  "certificate_id": "READY-{session_id[:8]}",
  "generated_for": "voter",
  "readiness_summary": {{
    "overall_score": 0,
    "status": "assessment_complete",
    "completed_steps": 0,
    "total_steps": 0
  }},
  "verified_areas": [
    "Legal eligibility check passed",
    "Age proof verified",
    "Aadhar card present"
  ],
  "pending_actions": [
    "Arrange hostel address proof",
    "Submit Form 6 online"
  ],
  "confidence_level": "moderate",
  "issued_at": "{timestamp}",
  "official_references": ["voters.eci.gov.in", "1950 helpline"]
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


# ─────────────────────────────────────────────
# PREDICTION AGENT PROMPTS
# ─────────────────────────────────────────────

def get_failure_risks_prompt(location: str, age: any, residence: str,
                             voter_status: str, document_concerns: list,
                             risk_factors: list) -> str:
    """Prompt for predicting voter failure risks."""
    return f"""
Analyze this voter profile for potential failure risks during the Indian election process.

Profile:
- Location: {location}
- Age: {age}
- Residence: {residence}
- Voter Status: {voter_status}
- Document Concerns: {document_concerns}
- Risk Factors: {risk_factors}

Return this exact JSON:
{{
  "profile_type": "first_time_student_hostel",
  "risk_assessment": {{
    "overall_risk_level": "medium",
    "risk_factors": [
      {{
        "factor": "Address proof for hostel residents",
        "risk_level": "high",
        "probability": 0.8,
        "impact": "Registration rejection or delay",
        "explanation": "Hostel residents often submit incorrect address proof",
        "similar_users_affected": true,
        "preventive_action": "Obtain official hostel certificate from warden"
      }}
    ]
  }},
  "corrective_mission": {{
    "mission_title": "Fix Your Address Proof",
    "description": "Complete this mission to get your hostel address proof ready",
    "steps": ["Meet hostel warden", "Get certificate on letterhead", "Scan clearly"],
    "estimated_time": "1 day"
  }},
  "recommendations": ["Start registration immediately", "Keep multiple document copies"],
  "prediction_confidence": "high"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""


# ─────────────────────────────────────────────
# SAFETY AGENT PROMPTS
# ─────────────────────────────────────────────

def get_safety_check_prompt(text: str) -> str:
    """Prompt for checking content safety."""
    return f"""
Analyze this text for safety issues in election information context.

Text: "{text}"

Return JSON:
{{
  "is_safe": true,
  "has_political_bias": false,
  "has_misinformation": false,
  "has_harmful_content": false,
  "risk_level": "low",
  "reason": "explanation here",
  "safe_alternatives": []
}}

IMPORTANT: Return only valid JSON. No markdown. No extra text.
"""


# ─────────────────────────────────────────────
# ACCESSIBILITY AGENT PROMPTS
# ─────────────────────────────────────────────

def get_micro_guidance_prompt(step_title: str, step_description: str) -> str:
    """Prompt for creating micro-guidance for a step."""
    return f"""
Create simple step-by-step guidance for this election step.

Step Title: {step_title}
Step Description: {step_description}

Return this exact JSON:
{{
  "step_title": "{step_title}",
  "simple_instructions": [
    "Instruction 1 - one simple sentence with action",
    "Instruction 2 - one simple sentence with action",
    "Instruction 3 - one simple sentence with action"
  ],
  "what_you_need": ["item 1", "item 2"],
  "time_needed": "X minutes",
  "common_mistake": "one common mistake to avoid",
  "encouragement": "one motivational line"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""