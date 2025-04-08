from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableMap

# Define prompt template
prompt = PromptTemplate.from_template("What is a good name for a company that makes {product}?")

# Define a chain that passes original input and formatted prompt together
chain = RunnableMap({
    "formatted_prompt": prompt,
    "product": lambda x: x["product"]
}) | RunnableLambda(lambda x: {
    "output": x["product"].upper() + " INC.",
    "prompt": x["formatted_prompt"]
})

# Run it
print(chain.invoke({"product": "AI-powered notebooks"}))
