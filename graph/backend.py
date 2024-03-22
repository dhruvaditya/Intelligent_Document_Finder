from fastapi import FastAPI
import uvicorn
app= FastAPI()
@app.get('/testing')
def test():
    return {"Hello":"world"}

# if __name__ =="__main__":
#     uvicorn.run(app, host="0.0.0.0", log_level="info")