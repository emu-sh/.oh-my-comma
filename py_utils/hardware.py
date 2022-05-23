import os

TICI = os.path.isfile('/TICI')
EON = os.path.isfile('/EON')
PC = not (TICI or EON)
