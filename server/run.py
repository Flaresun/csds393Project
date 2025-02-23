import uvicorn
import prisma
import subprocess

if __name__ == "__main__":
    # Generate Prisma Client
    subprocess.run(["prisma", "generate"])

    # Apply Migrations
    subprocess.run(["prisma", "migrate", "dev", "--name", "init"])
    
    # Run FastAPI
    uvicorn.run("main:app", reload=True)