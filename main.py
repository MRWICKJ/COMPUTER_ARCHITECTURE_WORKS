import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
# Import ReportLab's internal utility to safely read real image aspect ratios
from reportlab.lib.utils import ImageReader

def get_proportional_image(img_path, max_width=460, max_height=220):
    """
    Opens the image file, reads its real dimensions, and scales it down
    proportionally so it fits the PDF width/height limits without distorting.
    """
    try:
        img_reader = ImageReader(img_path)
        img_w, img_h = img_reader.getSize()
        
        # Calculate aspect ratio scaling factors
        aspect = img_w / float(img_h)
        
        # Start with max width boundary
        width = max_width
        height = max_width / aspect
        
        # If height exceeds our safe page space limit, scale down by height instead
        if height > max_height:
            height = max_height
            width = max_height * aspect
            
        return Image(img_path, width=width, height=height)
    except Exception as e:
        print(f"Error reading aspect ratio for {img_path}: {e}")
        # Fallback to standard standard image placeholder if it fails to open
        return Image(img_path, width=max_width, height=max_height)

def generate_pdf_manual(root_dir=".", output_pdf="Computer_Architecture_Lab_Manual.pdf"):
    folders = ["GATES", "ADDER", "SUBTRACTOR", "MUX", "DEMUX"]
    
    objectives = {

    "GATES": "To design, simulate, and verify basic and universal logic gates (AND, OR, NOT, NAND, NOR, XOR, XNOR) using Verilog HDL dataflow modeling.",

    "HALF_ADDER": "To design, simulate, and verify a 1-bit Half Adder using Verilog HDL dataflow modeling and analyze the Sum and Carry outputs.",

    "FULL_ADDER": "To design, simulate, and verify a 1-bit Full Adder using Verilog HDL dataflow modeling and analyze the Sum and Carry outputs with Carry-in input.",

    "HALF_SUBTRACTOR": "To design, simulate, and verify a 1-bit Half Subtractor using Verilog HDL dataflow modeling and analyze the Difference and Borrow outputs.",

    "FULL_SUBTRACTOR": "To design, simulate, and verify a 1-bit Full Subtractor using Verilog HDL dataflow modeling and analyze the Difference and Borrow outputs with Borrow-in input.",

    "MUX_2X1": "To design, simulate, and verify a 2x1 Multiplexer using Verilog HDL dataflow modeling and observe data selection through a single select line.",

    "MUX_4X1": "To design, simulate, and verify a 4x1 Multiplexer using Verilog HDL dataflow modeling and observe data selection through two select lines.",

    "MUX_8X1": "To design, simulate, and verify an 8x1 Multiplexer using Verilog HDL dataflow modeling and observe data selection through three select lines.",

    "DEMUX_1X2": "To design, simulate, and verify a 1x2 Demultiplexer using Verilog HDL dataflow modeling and route a single input to one of two outputs.",

    "DEMUX_1X4": "To design, simulate, and verify a 1x4 Demultiplexer using Verilog HDL dataflow modeling and route a single input to one of four outputs.",

    "DEMUX_1X8": "To design, simulate, and verify a 1x8 Demultiplexer using Verilog HDL dataflow modeling and route a single input to one of eight outputs."

}

    # Setup document geometry definitions
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Uniform Typography Stylesheet
    title_style = ParagraphStyle(
        'CoverTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=26, leading=30, alignment=1, spaceAfter=15
    )
    subtitle_style = ParagraphStyle(
        'CoverSub', parent=styles['Normal'], fontName='Courier-Bold', fontSize=11, alignment=1, textColor=colors.HexColor("#555555")
    )
    exp_title_style = ParagraphStyle(
        'ExpTitle', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=14, leading=18, spaceAfter=8, textColor=colors.HexColor("#111111")
    )
    body_style = ParagraphStyle(
        'ExpBody', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, spaceAfter=12, textColor=colors.HexColor("#333333")
    )
    section_label = ParagraphStyle(
        'SecLabel', fontName='Courier-Bold', fontSize=10, leading=12, spaceBefore=8, spaceAfter=6, textColor=colors.HexColor("#111111")
    )
    missing_style = ParagraphStyle(
        'MissingAsset', fontName='Courier', fontSize=9, leading=12, alignment=1, textColor=colors.HexColor("#888888")
    )

    story = []

    # --- COVER PAGE ---
    story.append(Spacer(1, 150))
    story.append(Paragraph("COMPUTER ARCHITECTURE<br/>LABORATORY MANUAL", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("DIGITAL LOGIC SIMULATION RECORDS", subtitle_style))
    story.append(PageBreak())

    def find_paired_assets(f_path):
        if not os.path.exists(f_path):
            return {}
        files = os.listdir(f_path)
        pairs = {}
        for f in files:
            match = re.search(r'([A-Za-z0-9_]+)_(CODE|OUTPUT)', f, re.IGNORECASE)
            if match:
                key = match.group(1).upper()
                type_suffix = match.group(2).upper()
                
                if "ALL_GATES" in key or "GATES" in key:
                    key = "GATES"
                
                if key not in pairs:
                    pairs[key] = {'code': None, 'output': None}
                
                if type_suffix == 'CODE':
                    pairs[key]['code'] = f
                elif type_suffix == 'OUTPUT':
                    pairs[key]['output'] = f
        return pairs

    exp_counter = 1
    
    for folder in folders:
        f_path = os.path.join(root_dir, folder)
        paired_assets = find_paired_assets(f_path)
        
        # Sort keys to ensure Half paths come before Full layout routes
        for key in sorted(paired_assets.keys(), reverse=True if folder in ["ADDER", "SUBTRACTOR"] else False):
            asset = paired_assets[key]
            obj_text = objectives.get(key, f"To study and verify performance logic parameters for the {key} module.")
            
            display_title = key.replace('_', ' ')
            story.append(Paragraph(f"EXPERIMENT {exp_counter}: Implementation of {display_title}", exp_title_style))
            story.append(Paragraph(f"<b>Objective:</b> {obj_text}", body_style))
            story.append(Spacer(1, 5))
            
            # Code Screen Capture Block
            story.append(Paragraph("--- Verilog Hardware Description Code ---", section_label))
            if asset['code']:
                img_path = os.path.join(f_path, asset['code'])
                # Generates proportional images dynamically
                img_flowable = get_proportional_image(img_path, max_width=460, max_height=220)
                img_flowable.hAlign = 'CENTER'
                story.append(img_flowable)
            else:
                story.append(Paragraph(f"[ File Missing: Code screenshot for {key} not found ]", missing_style))
            
            story.append(Spacer(1, 10))
            
            # Waveform Screen Capture Block
            story.append(Paragraph("--- Simulation Waveform Output Trace ---", section_label))
            if asset['output']:
                out_path = os.path.join(f_path, asset['output'])
                # Generates proportional images dynamically
                out_flowable = get_proportional_image(out_path, max_width=460, max_height=200)
                out_flowable.hAlign = 'CENTER'
                story.append(out_flowable)
            else:
                story.append(Paragraph(f"[ File Missing: Simulation trace screenshot for {key} not found ]", missing_style))
            
            story.append(PageBreak())
            exp_counter += 1

    if story and isinstance(story[-1], PageBreak):
        story.pop()

    doc.build(story)
    print(f"\n Success! Lab manual generated at '{output_pdf}' with perfect image proportions.")

if __name__ == '__main__':
    generate_pdf_manual(root_dir=".", output_pdf="Computer_Architecture_Lab_Manual.pdf")