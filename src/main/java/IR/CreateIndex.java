package IR;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;

import java.nio.file.Paths;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.document.StringField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

public class CreateIndex
{
    private String corpusPath;

    // Directory where the search index will be saved
    private static String INDEX_DIRECTORY = "index";
    public String getCorpusPath() {
        return corpusPath;
    }

    public void setCorpusPath(String path) {
        this.corpusPath = path;
    }

    public CreateIndex(String path, Analyzer analyzer) {
        setCorpusPath(path);
        System.out.println("DEBUG " + getCorpusPath());
        try {
            parseCorpusAndIndex(analyzer);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }

    public void parseCorpusAndIndex(Analyzer analyzer) throws IOException {
        Directory directory = FSDirectory.open(Paths.get(INDEX_DIRECTORY));
        IndexWriterConfig config = new IndexWriterConfig(analyzer);

        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE);

        IndexWriter iwriter = new IndexWriter(directory, config);

        // File opening Setup
        FileInputStream fstream = new FileInputStream(getCorpusPath());
        BufferedReader br = new BufferedReader(new InputStreamReader(fstream));

        String strLine;
        String currentTag = "ID"; // Assumption document starts with ID
        String previousTag = "";
        String contentOfTag = "";
        Boolean startNewContent = true;
        Boolean firstIteration = true;

        // ArrayList of documents in the corpus
		ArrayList<Document> documents = new ArrayList<Document>();
        Document doc = new Document();

        System.out.println("Start of Parsing " + getCorpusPath() );

        //Read File Line By Line
        while ((strLine = br.readLine()) != null)   {
            if (isNewTag(strLine)) {
                previousTag = currentTag;
                currentTag = extractTagName(strLine);
                // currentTag will become equal to ID, Title, Author, Bibliography or Body
                if(!"ID".equals(previousTag)) {
                    doc.add(new TextField(previousTag, contentOfTag, Field.Store.YES));
                }
                if (isIdTag(strLine)) {
                    String docId = strLine.substring(3);
                    if (!firstIteration) {
                        documents.add(doc);
                    }
                    firstIteration = false;
                    doc = new Document();
                    doc.add(new StringField(currentTag, docId, Field.Store.YES));
                    System.out.println("Document " + docId + " indexed");
                }
                startNewContent = true;
            }
            else { // Need to buffer the content of the line
                if (startNewContent) {
                    contentOfTag = strLine;
                    startNewContent = false;
                }
                else {
                    contentOfTag = contentOfTag + "\n" + strLine;
                }
            }
        }

        // Index the last tag
        doc.add(new TextField(currentTag, contentOfTag, Field.Store.YES));
        documents.add(doc);

        // Save the documents to the index
        iwriter.addDocuments(documents);

        // Commit changes and close everything
        iwriter.close();
        directory.close();
        System.out.println("End of Parsing & Indexing");

        fstream.close();
    }

    public String extractTagName(String tag) {
        if (isIdTag(tag)) {
            return "ID";
        }
        else if (isTitleTag(tag)) {
            return "Title";
        }
        else if (isAuthorTag(tag)) {
            return "Author";
        }
        else if (isBibTag(tag)) {
            return "Bibliography";
        }
        else {
            return "Body";
        }
    }

    public boolean isNewTag(String line) {
        return isIdTag(line) || isTitleTag(line) || isAuthorTag(line) || isBibTag(line) || isBodyTag(line);
    }

    public boolean isIdTag(String line) {
        return line.startsWith(".I");
    }

    public boolean isTitleTag(String line) {
        return line.startsWith(".T");
    }

    public boolean isAuthorTag(String line) {
        return line.startsWith(".A");
    }

    public boolean isBibTag(String line) {
        return line.startsWith(".B");
    }

    public boolean isBodyTag(String line) {
        return line.startsWith(".W");
    }
}
