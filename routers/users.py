from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    pass


@router.post("/login")
async def login():
    pass


@router.get("/")
async def profile():
    pass


@router.put("/update")
async def update():
    pass


@router.post("/logout")
async def logout():
    pass
