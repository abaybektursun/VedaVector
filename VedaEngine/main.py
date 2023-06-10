from langchain.embeddings import LlamaCppEmbeddings
from sklearn.metrics.pairwise import cosine_similarity

class Vectorizer:
    def __init__(self, model_path):
        self.model_path = model_path
        self.llama = LlamaCppEmbeddings(model_path=model_path)

    def embed_documents(self, documents):
        return self.llama.embed_documents(documents)

if __name__ == "__main__":
    model_path = "Wizard-Vicuna-13B-Uncensored.ggmlv3.q4_0.bin"
    vectorizer = Vectorizer(model_path)
    
    
    text1 = "Her hand touched mine and I felt a shock of electricity run through my body."
    text2 = "Gently, she kissed me on the neck, wispering in my ear, 'I love you.'"
    text3 = "llama_model_load_internal: mem required  = 9031.70 MB (+ 3216.00 MB per state)"
    doc_result = vectorizer.embed_documents([text1, text2, text3])    


    # Cosine similarity betwenn text1, text2, and text3 and print the results
    similarity_mat = cosine_similarity(doc_result)
    # Print the similarity separately
    print("Similarity between text1 and text2: ", similarity_mat[0][1])
    print("Similarity between text1 and text3: ", similarity_mat[0][2])
    print("Similarity between text2 and text3: ", similarity_mat[1][2])


