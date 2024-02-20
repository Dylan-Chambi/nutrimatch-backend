
FOOD_DETECTION_TEMPLATE = """
This model serves as a food and dishes detection system. You can input an image and receive a list of identified food items and dishes present in the image. Each identified item includes the following attributes:

Name: The name of the food or dish
Size: The size of the food or dish
Size Unit: The unit of measurement for the size of the food or dish
Amount: The quantity of the food or dish
Seasonings: Any seasonings used in the food or dish
Confidence: The model's confidence level in the prediction
Ingredients: The ingredients used in the food or dish

Try to split into multiple food items that represent a dish.

Additionally, you need to provide a general description of the image and a boolean value indicating whether the image is a valid representation of food.

If the image does not contain identifiable food items, the model will return a boolean value indicating that the image is not valid for food identification and a error message explaining why the image is not valid.

Please use the following format instructions for generating the response: {format_instructions}
"""