from pathlib import Path
import os
pathlist = Path("QmbsZEvJE8EU51HCUHQg2aem9JNFmFHdva3tGVYutdCXHp").rglob('*')
for path in pathlist:
    try:
        os.remove(path)
    except:
        continue