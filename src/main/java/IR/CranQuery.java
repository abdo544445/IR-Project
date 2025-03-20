package IR;

class CranQuery {
    private int id;
    private String content;

    public CranQuery(int id, String content) {
        this.id = id;
        this.content = content;
    }

    public int getId() {
        return this.id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getContent() {
        return this.content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    @Override
    public String toString(){
        return "ID: " + getId() + "\n"
            +   "Content: " + getContent();
    }
}