def chunk_text(text: str, chunk_size: int = 500) -> list[str]:
    chuncks = []
    
    for i in range(0, len(text), chunk_size):
        chunk = text[i:i+chunk_size]
        chuncks.append(chunk)
        
    return chuncks
    
    