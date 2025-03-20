#!/usr/bin/env python3
import os
import sys
import argparse
import subprocess
import shutil
from web_crawler import AcademicCrawler

def setup_directories(output_dir):
    """
    Create necessary directories for the crawler and Java app
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "results"), exist_ok=True)

def run_crawler(args):
    """
    Run the web crawler with the specified arguments
    """
    print(f"Starting web crawler with {len(args.urls)} URLs")
    
    crawler = AcademicCrawler(
        start_urls=args.urls,
        output_dir=args.output,
        max_pages=args.max_pages,
        delay=args.delay,
        max_workers=args.workers
    )
    
    crawler.crawl()
    
    # Check if files were created
    cran_file = os.path.join(args.output, "cran.all.crawled")
    qry_file = os.path.join(args.output, "cran.qry.crawled")
    
    if not os.path.exists(cran_file) or not os.path.exists(qry_file):
        print("Error: Crawler did not produce the required files")
        return False
    
    # Copy files to the standard location if not already there
    if args.output != "src/main/resources/crawled":
        target_dir = "src/main/resources/crawled"
        os.makedirs(target_dir, exist_ok=True)
        
        shutil.copy2(cran_file, os.path.join(target_dir, "cran.all.crawled"))
        shutil.copy2(qry_file, os.path.join(target_dir, "cran.qry.crawled"))
    
    return True

def create_cranqrel(output_dir, num_docs=10, num_queries=5):
    """
    Create a simple cranqrel file for evaluation
    """
    cranqrel_path = os.path.join(output_dir, "cranqrel")
    
    with open(cranqrel_path, "w") as f:
        # For each query, mark some documents as relevant
        for q in range(1, num_queries + 1):
            # Mark a few documents as relevant with different scores
            for d in range(1, num_docs + 1):
                if (q + d) % 3 == 0:  # Simple rule to determine relevance
                    relevance = ((q + d) % 4) + 1  # Score between 1-4
                    f.write(f"{q} {d} {relevance}\n")
    
    print(f"Created sample cranqrel file at {cranqrel_path}")
    return cranqrel_path

def setup_for_java_app(output_dir):
    """
    Setup the crawled files for use by the Java application
    """
    # Create symbolic links or copy to standard locations
    cran_file = os.path.join(output_dir, "cran.all.crawled")
    qry_file = os.path.join(output_dir, "cran.qry.crawled")
    cranqrel_file = os.path.join(output_dir, "cranqrel")
    
    java_resources = "src/main/resources/cran"
    os.makedirs(java_resources, exist_ok=True)
    
    # Create backup of original files if they exist
    for filename in ["cran.all.1400", "cran.qry", "cranqrel"]:
        orig_path = os.path.join(java_resources, filename)
        if os.path.exists(orig_path):
            shutil.copy2(orig_path, os.path.join(java_resources, f"{filename}.backup"))
    
    # Rename crawled files to match expected names
    try:
        shutil.copy2(cran_file, os.path.join(java_resources, "cran.all.1400"))
        shutil.copy2(qry_file, os.path.join(java_resources, "cran.qry"))
        shutil.copy2(cranqrel_file, os.path.join(java_resources, "cranqrel"))
        
        print("Files prepared for Java application")
        return True
    except Exception as e:
        print(f"Error setting up files for Java app: {str(e)}")
        return False

def run_java_app():
    """
    Run the Java application with the crawled data
    """
    try:
        # Check if Maven is available
        subprocess.run(["mvn", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Run the Maven project
        print("Running Java application...")
        subprocess.run(["mvn", "clean", "compile", "exec:java", "-Dexec.mainClass=IR.App"], check=True)
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running Java application: {str(e)}")
        return False
    except FileNotFoundError:
        print("Maven not found. Please install Maven or run the Java application manually.")
        return False

def main():
    """
    Main function to run the crawler and prepare data for the Java app
    """
    parser = argparse.ArgumentParser(description="Run web crawler and prepare data for IR Java app")
    parser.add_argument("--urls", nargs="+", default=["https://arxiv.org/list/cs.IR/recent"], 
                      help="Starting URLs for crawling")
    parser.add_argument("--output", default="src/main/resources/crawled", 
                      help="Output directory")
    parser.add_argument("--max-pages", type=int, default=100, 
                      help="Maximum number of pages to crawl")
    parser.add_argument("--delay", type=float, default=1.0, 
                      help="Delay between requests in seconds")
    parser.add_argument("--workers", type=int, default=5, 
                      help="Number of concurrent workers")
    parser.add_argument("--run-java", action="store_true", 
                      help="Run the Java application after crawling")
    
    args = parser.parse_args()
    
    # Setup necessary directories
    setup_directories(args.output)
    
    # Run the crawler
    if not run_crawler(args):
        print("Crawler failed to complete successfully")
        return 1
    
    # Create cranqrel file for evaluation
    create_cranqrel(args.output)
    
    # Setup for Java app
    if not setup_for_java_app(args.output):
        print("Failed to setup files for Java application")
        return 1
    
    # Run Java app if requested
    if args.run_java:
        if not run_java_app():
            print("Failed to run Java application")
            return 1
    else:
        print("\nTo run the Java application with the crawled data:")
        print("1. mvn clean compile exec:java -Dexec.mainClass=IR.App")
        print("OR")
        print("2. Run this script with --run-java flag\n")
    
    print("Process completed successfully!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 