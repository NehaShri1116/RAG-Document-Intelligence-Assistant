from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from .vector_store import load_store


def build_chain():
    db = load_store()
    retriever = db.as_retriever(search_kwargs={"k": 3})

    llm = ChatOllama(model="llama3", temperature=0)

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question using only the context below.

        Context:
        {context}

        Question:
        {question}
        """
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain