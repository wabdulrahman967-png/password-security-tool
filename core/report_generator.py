import json
import os
from datetime import datetime
from typing import Dict

class ReportGenerator:
    """Generate and export security reports"""
    
    def __init__(self):
        self.report_dir = "data/reports"
        try:
            os.makedirs(self.report_dir, exist_ok=True)
        except:
            pass  # لو مش موجود
    
    def generate_report(self, data: Dict) -> str:
        """Generate a formatted report from analysis data"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""
=======================================
    PASSWORD SECURITY REPORT
    Generated: {timestamp}
=======================================

📊 STRENGTH ANALYSIS
├─ Strength Level: {data.get('strength', 'N/A')}
├─ Score: {data.get('score', 0)}/{data.get('max_score', 8)}
├─ Entropy: {data.get('entropy', 0)} bits
└─ Common Password: {'Yes ⚠️' if data.get('is_common', False) else 'No ✅'}

📋 CRITERIA CHECKLIST
"""
        for key, value in data.get('criteria', {}).items():
            icon = "✅" if value else "❌"
            report += f"├─ {icon} {key.replace('_', ' ').title()}\n"
        
        if data.get('feedback'):
            report += "\n💡 RECOMMENDATIONS\n"
            for f in data.get('feedback', []):
                report += f"├─ {f}\n"
        
        if data.get('breach_info'):
            report += f"""
🔍 BREACH CHECK
├─ Breached: {'Yes 🚨' if data['breach_info'].get('is_breached') else 'No ✅'}
├─ Times Found: {data['breach_info'].get('count', 0)}
"""
        
        report += f"""
=======================================
    Report ID: {datetime.now().strftime('%Y%m%d%H%M%S')}
=======================================
"""
        return report
    
    def save_report(self, data: Dict, format: str = 'txt') -> str:
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.report_dir}/report_{timestamp}.{format}"
        
        if format == 'txt':
            content = self.generate_report(data)
        elif format == 'json':
            content = json.dumps(data, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
        except:
            # لو مش قادر يكتب (في السحابة)، يرجع النص بس
            pass
        
        return filename
