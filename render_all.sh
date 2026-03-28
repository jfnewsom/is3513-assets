#!/bin/bash
cd "$(dirname "$0")"

echo "Re-rendering labs..."
for f in pages/labs/json/lab*_COMPLETE.json; do
    python3 render_lab.py "$f" && echo "  ✓ $f"
done

echo ""
echo "Re-rendering reading pages..."
python3 render_reading.py && echo "  ✓ all reading pages"

echo ""
echo "Re-rendering support pages..."
python3 render_support_page.py && echo "  ✓ all support pages"

echo ""
echo "Re-rendering module overviews..."
python3 render_module_overview.py && echo "  ✓ all module overviews"

echo ""
echo "Done. Push via GitHub Desktop."
