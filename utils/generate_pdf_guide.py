"""
PDF Guide Generator for Smart Crop AI Project.
Builds an academic presentation script and viva defense dossier using ReportLab.
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether,
    HRFlowable
)
from reportlab.pdfgen import canvas

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PDF = os.path.join(PROJECT_ROOT, "Smart_Crop_AI_Project_Presentation_Guide.pdf")


class NumberedCanvas(canvas.Canvas):
    """Custom canvas that computes total page count dynamically."""
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(54, 11 * 72 - 36, "Smart Crop AI — B.Tech AIML Major Project Presentation Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 11 * 72 - 42, 8.5 * 72 - 54, 11 * 72 - 42)
            
        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * 72 - 54, 36, footer_text)
        self.drawString(54, 36, "Confidential — Academic Project Dossier & Defense Script")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 8.5 * 72 - 54, 48)
        self.restoreState()


def build_pdf(filename: str = OUTPUT_PDF):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#064e3b")      # Deep forest green
    ACCENT = colors.HexColor("#059669")       # Emerald green
    LIGHT_BG = colors.HexColor("#f0fdf4")     # Light mint
    TEXT_DARK = colors.HexColor("#0f172a")    # Slate dark text
    MUTED = colors.HexColor("#475569")        # Slate gray
    BORDER_COLOR = colors.HexColor("#cbd5e1")

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=PRIMARY,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=ACCENT,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=ACCENT,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=TEXT_DARK,
        spaceAfter=6
    )

    speech_style = ParagraphStyle(
        "Speech_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=15,
        spaceAfter=3
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=TEXT_DARK
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=11,
        textColor=PRIMARY
    )

    callout_text = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#065f46")
    )

    story = []

    # Title & Banner
    story.append(Paragraph("Smart Crop AI: Recommendation System", title_style))
    story.append(Paragraph("<b>B.Tech AIML Major Project — Presentation Script & Defense Dossier</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceBefore=0, spaceAfter=10))

    # Meta Info Card Table
    meta_data = [
        [
            Paragraph("<b>Academic Degree:</b> B.Tech AIML", table_cell_style),
            Paragraph("<b>Target Application:</b> Precision Agriculture", table_cell_style)
        ],
        [
            Paragraph("<b>Primary Model:</b> Random Forest (99.55% F1)", table_cell_style),
            Paragraph("<b>Explainability:</b> SHAP Game-Theoretic TreeExplainer", table_cell_style)
        ],
        [
            Paragraph("<b>Dataset:</b> 2,200 Balanced Records (22 Crops)", table_cell_style),
            Paragraph("<b>Frameworks:</b> Python 3.12, Streamlit, Scikit-learn", table_cell_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#a7f3d0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#d1fae5")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Executive Summary
    story.append(Paragraph("1. Executive Summary & Objective", h1_style))
    story.append(Paragraph(
        "<b>Smart Crop AI</b> is an intelligent agricultural advisory system engineered to recommend the optimal crop variety based on measured soil macronutrients (Nitrogen, Phosphorus, Potassium) and local microclimatic parameters (Temperature, Humidity, Soil pH, and Rainfall). The platform addresses agricultural crises caused by unscientific monoculture, nutrient mismatch, and climate-induced crop failures by replacing guesswork with supervised machine learning and explainable artificial intelligence.",
        body_style
    ))

    # Section 2: Technology Stack
    story.append(Paragraph("2. Technology Stack & Frameworks", h1_style))
    tech_data = [
        [Paragraph("Layer", table_header_style), Paragraph("Technologies Used", table_header_style), Paragraph("Core Architectural Role", table_header_style)],
        [Paragraph("Language & Core", table_cell_bold), Paragraph("Python 3.11 / 3.12", table_cell_style), Paragraph("Underlying runtime and standard scientific libraries", table_cell_style)],
        [Paragraph("Machine Learning", table_cell_bold), Paragraph("Scikit-Learn, Joblib", table_cell_style), Paragraph("Pipelines, 5-fold cross-validation, model serialization", table_cell_style)],
        [Paragraph("Data Processing", table_cell_bold), Paragraph("Pandas, NumPy", table_cell_style), Paragraph("Tabular loading, stratified split, descriptive statistics", table_cell_style)],
        [Paragraph("Explainable AI", table_cell_bold), Paragraph("SHAP (Shapley Values)", table_cell_style), Paragraph("TreeExplainer for local feature attributions and waterfall logic", table_cell_style)],
        [Paragraph("Visualizations", table_cell_bold), Paragraph("Plotly, Matplotlib, Seaborn", table_cell_style), Paragraph("Interactive gauge, radar, confusion matrix heatmaps, box plots", table_cell_style)],
        [Paragraph("UI & Web Service", table_cell_bold), Paragraph("Streamlit Multi-Page Framework", table_cell_style), Paragraph("Responsive web dashboard with custom CSS theme", table_cell_style)]
    ]
    t_tech = Table(tech_data, colWidths=[110, 160, 234])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 10))

    # Section 3: Empirical Model Benchmarks
    story.append(Paragraph("3. Empirical Machine Learning Model Benchmarks", h1_style))
    story.append(Paragraph(
        "Five algorithms were benchmarked on the 2,200-sample dataset using an 80/20 stratified split. Distance-based models (KNN, SVM) utilized StandardScaler inside pipelines to prevent data leakage.",
        body_style
    ))

    metric_data = [
        [
            Paragraph("Algorithm", table_header_style),
            Paragraph("Accuracy", table_header_style),
            Paragraph("Precision", table_header_style),
            Paragraph("Recall", table_header_style),
            Paragraph("F1-Score", table_header_style),
            Paragraph("5-Fold CV Accuracy", table_header_style)
        ],
        [
            Paragraph("<b>Random Forest (Best)</b>", table_cell_bold),
            Paragraph("99.55%", table_cell_style),
            Paragraph("99.57%", table_cell_style),
            Paragraph("99.55%", table_cell_style),
            Paragraph("<b>99.55%</b>", table_cell_bold),
            Paragraph("99.38% ± 0.61%", table_cell_style)
        ],
        [
            Paragraph("Gaussian Naive Bayes", table_cell_style),
            Paragraph("99.55%", table_cell_style),
            Paragraph("99.59%", table_cell_style),
            Paragraph("99.55%", table_cell_style),
            Paragraph("99.54%", table_cell_style),
            Paragraph("99.49% ± 0.42%", table_cell_style)
        ],
        [
            Paragraph("Support Vector Machine (SVM)", table_cell_style),
            Paragraph("98.86%", table_cell_style),
            Paragraph("98.96%", table_cell_style),
            Paragraph("98.86%", table_cell_style),
            Paragraph("98.87%", table_cell_style),
            Paragraph("98.24% ± 0.49%", table_cell_style)
        ],
        [
            Paragraph("K-Nearest Neighbors (KNN)", table_cell_style),
            Paragraph("98.18%", table_cell_style),
            Paragraph("98.29%", table_cell_style),
            Paragraph("98.18%", table_cell_style),
            Paragraph("98.16%", table_cell_style),
            Paragraph("96.82% ± 1.17%", table_cell_style)
        ],
        [
            Paragraph("Decision Tree Classifier", table_cell_style),
            Paragraph("97.95%", table_cell_style),
            Paragraph("98.06%", table_cell_style),
            Paragraph("97.95%", table_cell_style),
            Paragraph("97.94%", table_cell_style),
            Paragraph("98.52% ± 0.68%", table_cell_style)
        ]
    ]
    t_metric = Table(metric_data, colWidths=[140, 65, 65, 65, 65, 104])
    t_metric.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_BG, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_metric)
    story.append(Spacer(1, 12))

    # Page Break for the Oral Presentation Script
    story.append(PageBreak())

    # Section 4: Word-For-Word Presentation Script
    story.append(Paragraph("4. Word-For-Word Oral Presentation Script", h1_style))
    story.append(Paragraph(
        "<i>Use this timed transcript during your presentation. Speak clearly, maintaining eye contact and pointing to the dashboard elements.</i>",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Script Phase 1
    story.append(Paragraph("Phase 1: Greeting & Project Hook (0:00 - 0:45)", h2_style))
    box1 = [
        [Paragraph(
            "\"Good morning/afternoon respected teachers and examiners. Today, I am proud to present my B.Tech Major Project: <b>Smart Crop AI — An Intelligent Crop Recommendation System Using Machine Learning and Explainable AI</b>.<br/><br/>"
            "In traditional agriculture, crop selection predominantly relies on ancestral guesswork, regional habits, or trial-and-error. This causes severe soil exhaustion from chemical nutrient depletion and crop failure when weather-sensitive crops meet erratic rainfall. Our objective was to develop a scientific, data-driven system that accepts 7 physical parameters—Nitrogen, Phosphorus, Potassium, Soil pH, Temperature, Humidity, and Rainfall—to accurately recommend the optimal crop cultivar with probabilistic confidence and full algorithmic transparency.\"",
            speech_style
        )]
    ]
    t_box1 = Table(box1, colWidths=[504])
    t_box1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box1)
    story.append(Spacer(1, 8))

    # Script Phase 2
    story.append(Paragraph("Phase 2: Tech Stack, Dataset & Methodology (0:45 - 1:30)", h2_style))
    box2 = [
        [Paragraph(
            "\"We implemented the system in Python 3.12, utilizing Scikit-learn and Joblib for machine learning pipelines, Streamlit for the responsive UI, Plotly for dynamic interactive charting, and SHAP for explainable AI.<br/><br/>"
            "We trained our models on a benchmark agricultural dataset of 2,200 curated records across 22 balanced crop classes, with zero missing values. To completely eliminate data leakage, we enforced an 80/20 stratified split and encapsulated StandardScaler preprocessing directly within Scikit-learn Pipeline constructs.\"",
            speech_style
        )]
    ]
    t_box2 = Table(box2, colWidths=[504])
    t_box2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box2)
    story.append(Spacer(1, 8))

    # Script Phase 3
    story.append(Paragraph("Phase 3: Model Comparison & Findings (1:30 - 2:30)", h2_style))
    box3 = [
        [Paragraph(
            "\"We trained and compared 5 distinct classification paradigms: Random Forest, Gaussian Naive Bayes, Support Vector Machines, KNN, and Decision Trees.<br/><br/>"
            "As displayed on our Model Comparison dashboard, <b>Random Forest achieved the highest generalization benchmark with an Accuracy and F1-Score of 99.55%</b> and a 5-Fold Cross-Validation accuracy of 99.38%. Random Forest excels because agricultural parameters exhibit non-linear multi-threshold boundaries—for example, Rice requires high rainfall above 200 mm combined with humidity above 80%. An ensemble of 100 decorrelated bagged decision trees effectively models these complex interactions without overfitting.\"",
            speech_style
        )]
    ]
    t_box3 = Table(box3, colWidths=[504])
    t_box3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box3)
    story.append(Spacer(1, 8))

    # Script Phase 4
    story.append(Paragraph("Phase 4: Live Demonstration & Key Innovations (2:30 - 4:00)", h2_style))
    box4 = [
        [Paragraph(
            "\"Let me walk you through the live application modules:<br/>"
            "• <b>Inference Engine:</b> Accepts user soil inputs or agricultural presets. It renders the recommended crop, confidence gauge (e.g. 90%), top 3 secondary alternative crops, and a polar radar chart benchmarking user inputs against optimal conditions.<br/>"
            "• <b>Explainable AI (SHAP):</b> Using TreeExplainer, the system computes the exact game-theoretic force of each feature, showing why a crop was selected via bidirectional waterfall plots.<br/>"
            "• <b>Parameter Sensitivity Simulator:</b> Demonstrates whether varying a parameter by ±20% causes the crop recommendation to remain stable or transition to a different cultivar.<br/>"
            "• <b>Crop Knowledge Base:</b> Detailed cultivation guides and agronomic literature for all 22 crops.<br/>"
            "• <b>Audit Trail:</b> Tracks all session predictions with a single-click CSV export.\"",
            speech_style
        )]
    ]
    t_box4 = Table(box4, colWidths=[504])
    t_box4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box4)
    story.append(Spacer(1, 8))

    # Script Phase 5
    story.append(Paragraph("Phase 5: Conclusion & Future Scope (4:00 - 4:30)", h2_style))
    box5 = [
        [Paragraph(
            "\"In conclusion, Smart Crop AI delivers a production-grade, highly interpretable decision support platform. In future phases, this can be coupled with IoT soil probes for telemetry and weather APIs to auto-populate parameters via GPS coordinates. Thank you, I am now ready for questions.\"",
            speech_style
        )]
    ]
    t_box5 = Table(box5, colWidths=[504])
    t_box5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_box5)
    story.append(Spacer(1, 10))

    # Page Break for Viva Q&A
    story.append(PageBreak())

    # Section 5: Top 5 Examiner Questions & Answers
    story.append(Paragraph("5. Viva-Voce Defense: Top 5 Examiner Questions", h1_style))
    story.append(Paragraph(
        "<i>These are the most critical technical questions examiners ask during ML major project vivas. Memorize these points.</i>",
        body_style
    ))
    story.append(Spacer(1, 6))

    qa_list = [
        (
            "Q1: Why did you NOT include geographic location (GPS / State / District) as an ML input feature?",
            "Plant biology is governed strictly by physical soil chemistry and microclimatic thermodynamics, not administrative borders. Soil and rainfall vary drastically within a 10 km radius. Using 'District' as an ML feature would cause the model to memorize regional historical monoculture habits rather than scientific suitability. In our architecture, location serves as an upstream API layer to auto-fetch the 7 physical parameters."
        ),
        (
            "Q2: How did you ensure zero data leakage during data preprocessing?",
            "We applied stratified 80/20 train-test splitting strictly BEFORE any feature scaling or modeling. Furthermore, we encapsulated StandardScaler within Scikit-learn Pipeline objects. This guarantees that the mean and standard deviation are computed solely on the training fold, and test/validation folds are never seen during parameter fitting."
        ),
        (
            "Q3: Why use SHAP when Random Forest already provides Feature Importances?",
            "Gini feature importance provides only a global average of split frequencies across all 100 trees, but CANNOT explain an individual prediction for a specific farmer. SHAP applies cooperative game theory (Shapley values) to compute the exact marginal contribution of each physical factor for a single farm, showing whether high Nitrogen acted as a catalyst or if low rainfall restricted confidence."
        ),
        (
            "Q4: Why did Gaussian Naive Bayes achieve 99.54% accuracy despite the independence assumption?",
            "Naive Bayes assumes features are conditionally independent given the crop label. In agricultural ecology, crops occupy well-segregated nutrient niches (e.g. Apples uniquely require high Potassium and cool temps; Rice requires high water and heat). Because crop clusters are naturally isolated in 7D space, the conditional independence assumption holds remarkably well."
        ),
        (
            "Q5: Why did you choose Random Forest over Deep Neural Networks (MLP)?",
            "For tabular datasets with continuous physical features and moderate record counts (2,200 rows), tree ensembles consistently outperform deep neural networks in training efficiency, hyperparameter stability, and resistance to overfitting. Furthermore, Random Forest natively integrates with SHAP TreeExplainer for instantaneous local interpretability, whereas Deep Learning acts as a computationally heavier black box."
        )
    ]

    for q, a in qa_list:
        qa_data = [
            [Paragraph(f"<b>{q}</b>", ParagraphStyle("QA_Q", parent=h2_style, textColor=PRIMARY, fontSize=10, leading=13))],
            [Paragraph(f"<b>Defense:</b> {a}", body_style)]
        ]
        t_qa = Table(qa_data, colWidths=[504])
        t_qa.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.HexColor("#e2e8f0")),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_qa)
        story.append(Spacer(1, 6))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF at: {filename}")


if __name__ == "__main__":
    build_pdf()
