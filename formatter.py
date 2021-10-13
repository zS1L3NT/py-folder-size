def format(size: int) -> str:
    if size < 100:
        return str(size) + " B"

    if size < 1_000:
        return str(size) + " B"
    
    if size < 10_000:
        return str(round(size / 1_000, 3)) + " kB"

    if size < 100_000:
        return str(round(size / 1_000, 2)) + " kB"

    if size < 1_000_000:
        return str(round(size / 1_000, 1)) + " kB"
    
    if size < 10_000_000:
        return str(round(size / 1_000_000, 3)) + " MB"
    
    if size < 100_000_000:
        return str(round(size / 1_000_000, 2)) + " MB"
    
    if size < 1_000_000_000:
        return str(round(size / 1_000_000, 1)) + " MB"
    
    if size < 10_000_000_000:
        return str(round(size / 1_000_000_000, 3)) + " GB"
    
    if size < 100_000_000_000:
        return str(round(size / 1_000_000_000, 2)) + " GB"
    
    if size < 1_000_000_000_000:
        return str(round(size / 1_000_000_000, 1)) + " GB"
    
    if size < 10_000_000_000_000:
        return str(round(size / 1_000_000_000_000, 3)) + " TB"
    
    return "?"