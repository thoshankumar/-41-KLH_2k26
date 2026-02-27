"""
PDF Report Generator Module
Generates comprehensive financial health reports
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
from modules.health_score import HealthScoreEngine
from modules.prediction import OverspendPredictor
from modules.analytics import FinancialAnalytics
from modules.behavior_engine import BehaviorEngine
from modules.anomaly import AnomalyDetector
from config import REPORT_TITLE, REPORT_SUBTITLE


class ReportGenerator:
    """Generate PDF financial reports"""
    
    def __init__(self, user_id, user_name, user_email):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        
        # Initialize modules
        self.health_engine = HealthScoreEngine(user_id)
        self.predictor = OverspendPredictor(user_id)
        self.analytics = FinancialAnalytics(user_id)
        self.behavior_engine = BehaviorEngine(user_id)
        self.anomaly_detector = AnomalyDetector(user_id)
    
    def generate_pdf_report(self):
        """
        Generate comprehensive PDF report
        
        Returns:
            BytesIO buffer containing PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for flowables
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.grey,
            spaceAfter=20,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title
        story.append(Paragraph(REPORT_TITLE, title_style))
        story.append(Paragraph(REPORT_SUBTITLE, subtitle_style))
        story.append(Spacer(1, 0.2*inch))
        
        # User Info
        story.append(Paragraph(f"<b>Generated for:</b> {self.user_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Email:</b> {self.user_email}", styles['Normal']))
        story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", heading_style))
        summary = self._generate_executive_summary()
        story.append(Paragraph(summary, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Financial Health Score
        story.append(Paragraph("Financial Health Score", heading_style))
        score_data = self.health_engine.calculate_health_score()
        
        score_table_data = [
            ['Metric', 'Score', 'Grade'],
            ['Overall Health Score', f"{score_data['final_score']:.1f}/100", score_data['grade']],
            ['Delivery Ratio', f"{score_data['components']['delivery_ratio']['score']:.1f}/100", ''],
            ['Volatility', f"{score_data['components']['volatility']['score']:.1f}/100", ''],
            ['Anomaly Frequency', f"{score_data['components']['anomaly_frequency']['score']:.1f}/100", ''],
            ['Overspending Control', f"{score_data['components']['overspending']['score']:.1f}/100", '']
        ]
        
        score_table = Table(score_table_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#e6f2ff')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(score_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Overspending Risk
        story.append(Paragraph("Overspending Risk Analysis", heading_style))
        risk_data = self.predictor.predict_overspend_risk()
        
        risk_text = f"""
        <b>Risk Level:</b> {risk_data['risk_level']}<br/>
        <b>Probability:</b> {risk_data['risk_percentage']:.1f}%<br/>
        <br/>
        {self._format_risk_factors()}
        """
        story.append(Paragraph(risk_text, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Spending Breakdown
        story.append(Paragraph("Spending Analysis", heading_style))
        delivery_metrics = self.analytics.get_delivery_metrics()
        stats = self.analytics.get_summary_stats()
        
        spending_table_data = [
            ['Category', 'Value'],
            ['Total Spending', f"₹{stats['total_spent']:,.2f}"],
            ['Total Transactions', f"{stats['total_transactions']}"],
            ['Average Transaction', f"₹{stats['average_transaction']:,.2f}"],
            ['Delivery Spending', f"₹{delivery_metrics['delivery_total']:,.2f}"],
            ['Delivery %', f"{delivery_metrics['delivery_percentage']:.1f}%"],
        ]
        
        spending_table = Table(spending_table_data, colWidths=[3*inch, 3*inch])
        spending_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        story.append(spending_table)
        story.append(Spacer(1, 0.2*inch))
        
        # Historical Comparison
        previous_score = self.health_engine.get_previous_score()
        if previous_score:
            story.append(Paragraph("Historical Comparison", heading_style))
            comparison_text = f"""
            <b>Previous Score:</b> {previous_score['previous_score']:.1f}/100<br/>
            <b>Current Score:</b> {previous_score['current_score']:.1f}/100<br/>
            <b>Change:</b> {'+' if previous_score['change'] > 0 else ''}{previous_score['change']:.1f} points<br/>
            """
            story.append(Paragraph(comparison_text, styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
        
        # Recent Nudges
        story.append(Paragraph("Behavioral Insights & Nudges", heading_style))
        nudges = self.behavior_engine.get_recent_nudges(5)
        
        if nudges:
            for nudge in nudges:
                nudge_text = f"• {nudge['nudge_text']}"
                story.append(Paragraph(nudge_text, styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        else:
            story.append(Paragraph("No behavioral nudges generated yet.", styles['Normal']))
        
        story.append(Spacer(1, 0.2*inch))
        
        # Recommendations
        story.append(Paragraph("Recommendations", heading_style))
        recommendations = self.predictor.get_recommendations()
        
        for rec in recommendations:
            story.append(Paragraph(f"• {rec}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        # Footer
        story.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        story.append(Paragraph(
            f"Generated by Real-time Budget Nudge Agent • {datetime.now().strftime('%B %d, %Y %H:%M')}",
            footer_style
        ))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _generate_executive_summary(self):
        """Generate AI executive summary"""
        score_data = self.health_engine.calculate_health_score()
        delivery_metrics = self.analytics.get_delivery_metrics()
        risk_data = self.predictor.predict_overspend_risk()
        
        summary = f"""
        Your financial health score is <b>{score_data['final_score']:.1f}/100</b> ({score_data['status']}). 
        You have made {len(self.analytics.transactions_df)} transactions with delivery orders representing 
        <b>{delivery_metrics['delivery_percentage']:.1f}%</b> of your total spending. 
        Your overspending risk is assessed as <b>{risk_data['risk_level']}</b> with a 
        {risk_data['risk_percentage']:.1f}% probability. 
        """
        
        if score_data['final_score'] >= 80:
            summary += "You're maintaining excellent financial discipline. "
        elif score_data['final_score'] >= 60:
            summary += "There's room for improvement in your spending patterns. "
        else:
            summary += "Immediate attention needed to improve your financial health. "
        
        if delivery_metrics['delivery_percentage'] > 25:
            summary += f"Consider reducing delivery spending by cooking at home more often."
        
        return summary
    
    def _format_risk_factors(self):
        """Format risk factors for PDF"""
        risk_factors = self.predictor.get_risk_factors()
        
        if not risk_factors:
            return "<b>No major risk factors detected.</b>"
        
        text = "<b>Key Risk Factors:</b><br/>"
        for factor in risk_factors:
            text += f"• {factor['factor']}: {factor['value']} ({factor['severity']} severity)<br/>"
        
        return text
