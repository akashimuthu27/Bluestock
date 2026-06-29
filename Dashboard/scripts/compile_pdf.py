import os
import glob
import shutil
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages

# Define paths
brain_dir = r"C:\Users\AKASH\.gemini\antigravity\brain\2182f5ea-f1cd-4e47-a172-01e060727829"
base_dir = r"C:\Users\AKASH\Desktop\BLUESTOCK\Dashboard"
figures_dir = os.path.join(base_dir, "reports", "figures")
pdf_path = os.path.join(base_dir, "reports", "Dashboard.pdf")

os.makedirs(figures_dir, exist_ok=True)

print("Searching for generated dashboard images in brain directory...")

# Mapping of search patterns to target filenames
patterns = {
    "industry_overview_dashboard": "page1_industry_overview.png",
    "fund_performance_dashboard": "page2_fund_performance.png",
    "investor_analytics_dashboard": "page3_investor_analytics.png",
    "sip_market_trends_dashboard": "page4_market_trends.png"
}

copied_files = []

for prefix, target_name in patterns.items():
    search_pattern = os.path.join(brain_dir, f"{prefix}_*.png")
    matches = glob.glob(search_pattern)
    if matches:
        # Sort by modification time to get the latest one
        latest_match = max(matches, key=os.path.getmtime)
        target_path = os.path.join(figures_dir, target_name)
        shutil.copy2(latest_match, target_path)
        print(f"Copied: {os.path.basename(latest_match)} -> {target_name}")
        copied_files.append(target_path)
    else:
        print(f"WARNING: No matches found for pattern: {prefix}_*.png")

if len(copied_files) < 4:
    print(f"Error: Only found {len(copied_files)}/4 dashboard pages. Cannot compile PDF.")
    exit(1)

print("\nCompiling dashboard pages into a single PDF...")
try:
    from PIL import Image
    images = [Image.open(img_path).convert('RGB') for img_path in copied_files]
    # Save the first image as a PDF and append the rest
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"Dashboard PDF compiled successfully at: {pdf_path}")
except Exception as e:
    print(f"Error compiling PDF: {e}")
    exit(1)
