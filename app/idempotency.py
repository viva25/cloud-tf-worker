processed=set()
def already_processed(e): return e in processed
def mark_processed(e): processed.add(e)
