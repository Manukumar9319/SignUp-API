import uvicorn
from fastapi import FastAPI
from login import login_router, logout_router
from signUp import signUp_ops_router, signUp_client_router
app = FastAPI()

app.include_router(signUp_ops_router, prefix="/api/Ops_Signup")
app.include_router(signUp_client_router, prefix="/api/Client_Signup")
app.include_router(login_router, prefix="/api/login")
app.include_router(logout_router, prefix="/api/logout")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
