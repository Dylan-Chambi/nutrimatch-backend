import numpy as np
from trulens_eval import TruCustomApp
from trulens_eval import Select, Feedback
from trulens_eval.feedback import Groundedness
from trulens_eval.feedback.provider.openai import OpenAI as fOpenAI
from src.config.config import get_settings
from src.predictor.gpt_food_detector import GPTFoodDetector


SETTINGS = get_settings()


class DetectorTracking:
    def __init__(self):
        self.app_name = "Food Detector"
        self.food_detector = GPTFoodDetector()
        self.fopenai = fOpenAI(api_key=SETTINGS.OPENAI_KEY)
        self.grounded = Groundedness(groundedness_provider=self.fopenai)
        self.f_groundedness = (
            Feedback(self.grounded.groundedness_measure_with_cot_reasons, name = "Groundedness")
            .on(Select.RecordCalls.detect_food.rets.collect())
            .on_output()
            .aggregate(self.grounded.grounded_statements_aggregator)
        )
        self.f_qa_relevance = (
            Feedback(self.fopenai.relevance_with_cot_reasons, name = "Answer Relevance")
            .on(Select.RecordCalls.detect_food.args.detector_context_template)
            .on_output()
        )
        self.f_context_relevance = (
            Feedback(self.fopenai.qs_relevance_with_cot_reasons, name = "Context Relevance")
            .on(Select.RecordCalls.detect_food.args.detector_context_template)
            .on(Select.RecordCalls.detect_food.rets.collect())
            .aggregate(np.mean)
        )
        
        self.tru_llm_recorder = TruCustomApp(self.food_detector, app_id=self.app_name, feedbacks=[
            self.f_groundedness, self.f_qa_relevance, self.f_context_relevance
        ])