from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, 
from rasa_sdk.forms import FormValidationAction

# Authorized supplier list from CROaccess.com
AUTHORIZED_SUPPLIERS = [
    'Pylon Phenomics',
    'CROquest',
    'Novotech',
    'Allucent',
    'BioAgile',
    'Clario',
    'Fortrea',
    'Icon',
    'Parexel',
    'Thermo Fisher Scientific (PPD)',
    'Syneos Health',
    'Medpace',
    'Labcorp Drug Development',
    'Advanced Clinical',
    'Worldwide Clinical Trials'
]

# Supplier specializations and expertise
SUPPLIER_EXPERTISE = {
    'Pylon Phenomics': {
        'specialties': ['bioanalytical', 'single-cell analysis', 'spatial biology', 'assay development'],
        'therapeutic_areas': ['oncology', 'immunology', 'neuroscience'],
        'services': ['bioanalytical services', 'data management', 'assay development']
    },
    'CROquest': {
        'specialties': ['clinical trials', 'regulatory affairs', 'data management'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'immunology'],
        'services': ['clinical trial management', 'regulatory support', 'data management']
    },
    'Novotech': {
        'specialties': ['clinical trials', 'patient recruitment', 'site management'],
        'therapeutic_areas': ['oncology', 'cardiology', 'diabetes', 'respiratory'],
        'services': ['clinical trial management', 'patient recruitment', 'site management']
    },
    'Allucent': {
        'specialties': ['clinical development', 'regulatory affairs', 'biostatistics'],
        'therapeutic_areas': ['oncology', 'rare diseases', 'neurology'],
        'services': ['clinical trial management', 'regulatory support', 'biostatistics']
    },
    'BioAgile': {
        'specialties': ['preclinical', 'toxicology', 'assay development'],
        'therapeutic_areas': ['oncology', 'immunology', 'infectious diseases'],
        'services': ['preclinical research', 'toxicology studies', 'assay development']
    },
    'Clario': {
        'specialties': ['clinical trial technology', 'data management', 'eCOA'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'respiratory'],
        'services': ['clinical trial management', 'data management', 'patient reported outcomes']
    },
    'Fortrea': {
        'specialties': ['clinical trials', 'regulatory affairs', 'patient recruitment'],
        'therapeutic_areas': ['oncology', 'cardiology', 'diabetes', 'rare diseases'],
        'services': ['clinical trial management', 'regulatory support', 'patient recruitment']
    },
    'Icon': {
        'specialties': ['clinical trials', 'biostatistics', 'medical writing'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'immunology'],
        'services': ['clinical trial management', 'biostatistics', 'medical writing']
    },
    'Parexel': {
        'specialties': ['clinical trials', 'regulatory affairs', 'patient recruitment'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'rare diseases'],
        'services': ['clinical trial management', 'regulatory support', 'patient recruitment']
    },
    'Thermo Fisher Scientific (PPD)': {
        'specialties': ['clinical trials', 'laboratory services', 'bioanalytical'],
        'therapeutic_areas': ['oncology', 'cardiology', 'immunology', 'infectious diseases'],
        'services': ['clinical trial management', 'laboratory services', 'bioanalytical services']
    },
    'Syneos Health': {
        'specialties': ['clinical trials', 'commercialization', 'patient recruitment'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'respiratory'],
        'services': ['clinical trial management', 'patient recruitment', 'commercialization']
    },
    'Medpace': {
        'specialties': ['clinical trials', 'regulatory affairs', 'medical writing'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'rare diseases'],
        'services': ['clinical trial management', 'regulatory support', 'medical writing']
    },
    'Labcorp Drug Development': {
        'specialties': ['clinical trials', 'laboratory services', 'bioanalytical'],
        'therapeutic_areas': ['oncology', 'cardiology', 'immunology', 'infectious diseases'],
        'services': ['clinical trial management', 'laboratory services', 'bioanalytical services']
    },
    'Advanced Clinical': {
        'specialties': ['clinical trials', 'regulatory affairs', 'patient recruitment'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'immunology'],
        'services': ['clinical trial management', 'regulatory support', 'patient recruitment']
    },
    'Worldwide Clinical Trials': {
        'specialties': ['clinical trials', 'patient recruitment', 'site management'],
        'therapeutic_areas': ['oncology', 'cardiology', 'neurology', 'respiratory'],
        'services': ['clinical trial management', 'patient recruitment', 'site management']
    }
}

class ActionStartProjectScoping(Action):
    def name(self) -> Text:
        return "action_start_project_scoping"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Great! Let's start building your project scope. What phase of study are you planning? (e.g., Phase I, Phase II, Phase III, Phase IV, Preclinical)")
        return []

class ActionOutputProjectScope(Action):
    def name(self) -> Text:
        return "action_output_project_scope"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        study_phase = tracker.get_slot("study_phase")
        therapeutic_area = tracker.get_slot("therapeutic_area")
        services_needed = tracker.get_slot("services_needed")
        patient_population = tracker.get_slot("patient_population")
        timeline = tracker.get_slot("timeline")

        msg = "Project Scope:\n"
        if study_phase:
            msg += f"• Study Phase: {study_phase}\n"
        if therapeutic_area:
            msg += f"• Therapeutic Area: {therapeutic_area}\n"
        if services_needed:
            msg += f"• Services Needed: {', '.join(services_needed)}\n"
        if patient_population:
            msg += f"• Patient Population: {patient_population}\n"
        if timeline:
            msg += f"• Timeline: {timeline}\n"

        if msg.strip() == "Project Scope:":
            msg = "Project information is not available."

        dispatcher.utter_message(text=msg)
        return [SlotSet("project_scope_complete", True)]

class ActionMatchCROs(Action):
    def name(self) -> Text:
        return "action_match_cros"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        study_phase = tracker.get_slot("study_phase")
        therapeutic_area = tracker.get_slot("therapeutic_area")
        services_needed = tracker.get_slot("services_needed")
        patient_population = tracker.get_slot("patient_population")
        timeline = tracker.get_slot("timeline")
        
        # Score suppliers based on project requirements
        supplier_scores = []
        
        for supplier in AUTHORIZED_SUPPLIERS:
            score = 80  # Base score
            expertise = SUPPLIER_EXPERTISE.get(supplier, {})
            
            # Score based on therapeutic area match
            if therapeutic_area and therapeutic_area.lower() in [area.lower() for area in expertise.get('therapeutic_areas', [])]:
                score += 10
            
            # Score based on services match
            if services_needed:
                for service in services_needed:
                    if service.lower() in [s.lower() for s in expertise.get('services', [])]:
                        score += 5
            
            # Score based on study phase expertise
            if study_phase:
                if study_phase.lower() in ['phase i', 'phase 1', 'preclinical'] and 'preclinical' in expertise.get('specialties', []):
                    score += 5
                elif study_phase.lower() in ['phase ii', 'phase 2', 'phase iii', 'phase 3', 'phase iv', 'phase 4'] and 'clinical trials' in expertise.get('specialties', []):
                    score += 5
            
            # Score based on patient population expertise
            if patient_population:
                if patient_population.lower() in ['pediatric', 'children'] and 'pediatric' in expertise.get('specialties', []):
                    score += 3
                elif patient_population.lower() in ['elderly', 'seniors'] and 'geriatric' in expertise.get('specialties', []):
                    score += 3
            
            score = min(score, 100)
            
            if score >= 80:
                supplier_scores.append({
                    'name': supplier,
                    'score': score,
                    'reason': self._generate_reason(supplier, expertise, study_phase, therapeutic_area, services_needed)
                })
        
        # Sort by score and take top 5
        supplier_scores.sort(key=lambda x: x['score'], reverse=True)
        top_suppliers = supplier_scores[:5]
        
        # Format response
        msg = "Based on your project requirements, here are the top CRO matches:\n\n"
        for supplier in top_suppliers:
            msg += f"{supplier['name']} (Score: {supplier['score']})\n"
            msg += f"Reason: {supplier['reason']}\n\n"
        
        msg += "Please type the name of the CRO you'd like to select."
        dispatcher.utter_message(text=msg)
        return []

    def _generate_reason(self, supplier: str, expertise: Dict, study_phase: str, therapeutic_area: str, services_needed: List[str]) -> str:
        reasons = []
        
        if therapeutic_area and therapeutic_area.lower() in [area.lower() for area in expertise.get('therapeutic_areas', [])]:
            reasons.append(f"expertise in {therapeutic_area}")
        
        if services_needed:
            matched_services = []
            for service in services_needed:
                if service.lower() in [s.lower() for s in expertise.get('services', [])]:
                    matched_services.append(service)
            if matched_services:
                reasons.append(f"specializes in {', '.join(matched_services)}")
        
        if study_phase:
            if study_phase.lower() in ['phase i', 'phase 1', 'preclinical'] and 'preclinical' in expertise.get('specialties', []):
                reasons.append("strong preclinical capabilities")
            elif study_phase.lower() in ['phase ii', 'phase 2', 'phase iii', 'phase 3', 'phase iv', 'phase 4'] and 'clinical trials' in expertise.get('specialties', []):
                reasons.append("extensive clinical trial experience")
        
        if reasons:
            return f"{supplier} has {', '.join(reasons)}."
        else:
            return f"{supplier} offers comprehensive CRO services suitable for your project."

class ActionSendProject(Action):
    def name(self) -> Text:
        return "action_send_project"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        cro_name = tracker.get_slot("cro_name")
        study_phase = tracker.get_slot("study_phase")
        therapeutic_area = tracker.get_slot("therapeutic_area")
        services_needed = tracker.get_slot("services_needed")
        patient_population = tracker.get_slot("patient_population")
        timeline = tracker.get_slot("timeline")
        
        msg = (
            f"Perfect! Your project details have been sent to {cro_name}!\n\n"
            f"Project Summary:\n"
            f"• Study Phase: {study_phase}\n"
            f"• Therapeutic Area: {therapeutic_area}\n"
            f"• Services Needed: {', '.join(services_needed) if services_needed else 'Not specified'}\n"
            f"• Patient Population: {patient_population}\n"
            f"• Timeline: {timeline}\n\n"
            f"{cro_name} will contact you within 24-48 hours to discuss your project in detail."
        )
        dispatcher.utter_message(text=msg)
        return []

class ValidateProjectScopeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_project_scope_form"

    def validate_timeline(
        self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:
        value = value.strip()
        return {"timeline": value}
