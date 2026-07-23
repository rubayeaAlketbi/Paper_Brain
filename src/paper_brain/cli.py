import typer

# Creating and 
app = typer.Typer()

@app.command()
def add(arxiv_id:str, topic:str = "inbox"):
    ''' Added a paper to the library'''
    print(f"Adding {arxiv_id} to {topic}...")

@app.command()
def search(query:str, limit:int = 5):
    ''' Search for papers by query'''
    print(f"Searching for '{query}' with limit {limit}...")

@app.command()
def list():
    '''Listing all papers'''
    print("Listing all papers")
    
if __name__ == "__main__":
    app()
    