from typing import Dict, Any, List, Optional
import logging

from services.vertex_ai_service import vertex_ai_service
from utils.helpers import get_timestamp

# Setup logging
logger = logging.getLogger(__name__)


class SimulationAgent:
    """
    Agent 5 - Simulation Agent

    Responsibilities:
    - Run interactive mission scenarios
    - Simulate what-if situations
    - Create disruption scenarios and edge cases
    - Generate quiz questions for learning
    - Simulate poll day experience
    - Provide scenario based learning
    """

    SYSTEM_INSTRUCTION = """
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


    def generate_mission(
        self,
        mission_number: int,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate an interactive mission for the user.

        Args:
            mission_number: Mission number 1 to 5
            profile: User civic twin profile

        Returns:
            Complete mission with scenarios and questions
        """
        try:
            mission_topics = {
                1: "Eligibility and Registration Understanding",
                2: "Document Preparation Guidance",
                3: "Timeline and Deadline Awareness",
                4: "Poll Day Process Walkthrough",
                5: "Disruption Scenarios and Edge Cases"
            }

            topic = mission_topics.get(
                mission_number,
                "General Election Knowledge"
            )

            location = profile.get(
                "personal_info", {}
            ).get("location", "India")
            voter_status = profile.get(
                "voter_profile", {}
            ).get("voter_status", "first_time")

            prompt = f"""
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
  "learning_objectives": [
    "Objective 1",
    "Objective 2",
    "Objective 3"
  ],
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
  "key_takeaways": [
    "Key learning 1",
    "Key learning 2",
    "Key learning 3"
  ],
  "completion_message": "Encouraging message on mission completion",
  "next_mission_preview": "Brief preview of next mission"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
Make questions specific to Indian election process. Do not mention real political parties.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Generate mission error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def run_what_if_scenario(
        self,
        scenario: str,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Run a what-if scenario simulation.

        Args:
            scenario: The what-if scenario question
            profile: User civic twin profile

        Returns:
            Scenario simulation result with outcomes and solutions
        """
        try:
            location = profile.get(
                "personal_info", {}
            ).get("location", "India")

            prompt = f"""
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
    }},
    {{
      "outcome": "Alternative outcome",
      "probability": "medium",
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
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Run what-if scenario error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def simulate_poll_day(
        self,
        profile: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate the complete poll day experience.

        Args:
            profile: User civic twin profile

        Returns:
            Interactive poll day simulation
        """
        try:
            location = profile.get(
                "personal_info", {}
            ).get("location", "India")

            prompt = f"""
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
      "time": "8:15 AM",
      "event": "Queue and verification",
      "action": "Show your photo ID to polling officer",
      "tip": "Have your ID ready to avoid slowing the queue"
    }},
    {{
      "time": "8:20 AM",
      "event": "Ink marking",
      "action": "Get indelible ink mark on left index finger",
      "tip": "This prevents double voting"
    }},
    {{
      "time": "8:22 AM",
      "event": "Voting",
      "action": "Press the button on EVM next to your chosen candidate",
      "tip": "Take your time, no one can see your vote"
    }},
    {{
      "time": "8:25 AM",
      "event": "VVPAT verification",
      "action": "Check the slip shown for 7 seconds to verify",
      "tip": "This confirms your vote was recorded correctly"
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
    }},
    {{
      "situation": "Long queue and you need to leave",
      "solution": "Ask officials about the queue management system"
    }}
  ],
  "dos": [
    "Carry your voter ID or valid alternate photo ID",
    "Arrive early to avoid long queues",
    "Stay calm and patient in the queue"
  ],
  "donts": [
    "Do not carry mobile phone inside voting compartment",
    "Do not take photos of your vote",
    "Do not campaign within 100 meters of the booth"
  ],
  "emergency_contact": "1950 voter helpline"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Simulate poll day error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


    def check_answer(
        self,
        question_id: str,
        user_answer: str,
        correct_answer: str,
        explanation: str
    ) -> Dict[str, Any]:
        """
        Check user answer and provide feedback.

        Args:
            question_id: Question identifier
            user_answer: User provided answer
            correct_answer: Correct answer
            explanation: Explanation of correct answer

        Returns:
            Answer check result with feedback
        """
        try:
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()

            prompt = f"""
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
  "points_earned": {"10" if is_correct else "0"},
  "encouragement": "motivational message for the user"
}}

IMPORTANT: Return only valid JSON. No markdown. No trailing commas. No extra text.
"""
            result = vertex_ai_service.generate_structured(
                prompt=prompt,
                system_instruction=self.SYSTEM_INSTRUCTION
            )

            return {
                "success": True,
                "data": result,
                "timestamp": get_timestamp()
            }

        except Exception as e:
            logger.error(f"Check answer error: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Single instance
simulation_agent = SimulationAgent()