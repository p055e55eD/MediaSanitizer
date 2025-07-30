# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from scraper import NewsScraper
from analyzer import NewsAnalyzer
from report_gen import ReportGenerator
from database import db

app = Flask(__name__)
CORS(app)

scraper  = NewsScraper()
analyzer = NewsAnalyzer()
reporter = ReportGenerator()

@app.route('/api/analyze', methods=['POST'])
def analyze_article():
    start = datetime.now()
    data = request.get_json(force=True)
    app.logger.info(f"[API] Received payload: {data}")

    # Validate
    t = data.get("type")
    content = data.get("content","").strip()
    if t not in ("url","text") or not content:
        return jsonify(error="Invalid request"), 400

    # Prepare article_data
    if t == "url":
        # scraping logic...
        scraped = scraper.scrape(content)
        if not scraped:
            return jsonify(error="Failed to scrape article"), 400
        article_data = {
            "title":  scraped.get("title", ""),
            "content":scraped["content"],
            "domain": scraped.get("domain","")
        }
    else:  # text mode
        article_data = {
            "title":   "User Provided Text",
            "content": content,
            "domain":  "direct_input"
        }

    app.logger.info(f"[API] Article data ready (len={len(article_data['content'])})")

    # Analyze
    analysis = analyzer.analyze(article_data)
    if not analysis:
        app.logger.error("[API] Analyzer returned nothing")
        return jsonify(error="Failed to analyze article"), 500

    # Generate
    report = reporter.generate(analysis)
    if not report:
        app.logger.error("[API] Reporter returned nothing")
        return jsonify(error="Failed to generate report"), 500

    # Cache URL
    if t == "url":
        db.save_analysis(content, article_data["title"], article_data["domain"], article_data["content"], report)

    resp = {
        "status": "success",
        "result": report,
        "processing_time": str(datetime.now() - start)
    }
    app.logger.info(f"[API] Returning response: status=success")
    return jsonify(resp), 200

if __name__ == "__main__":
    app.run(debug=True)
