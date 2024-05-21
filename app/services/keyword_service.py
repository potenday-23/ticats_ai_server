# Modules
from fastapi import HTTPException
import requests


# Main Section
def get_evaluations(goods_code: str):
    base_url = "https://api-ticketfront.interpark.com/v1/boards"

    # 관람평 (boardNo: 62)
    expect_evaluation_url = f"{base_url}?best=false&notice=false&page=1&pageSize=60&sort=DESC_WRITE_DATE&boardNo=62&goodsCode={goods_code}"
    expect_evaluation_response = requests.get(expect_evaluation_url)

    if expect_evaluation_response.status_code != 200:
        raise HTTPException(status_code=expect_evaluation_response.status_code,
                            detail="Failed to fetch expect evaluations")

    expect_evaluation_text = ""
    expect_evaluation_data = expect_evaluation_response.json().get("data", [])
    for evaluation in expect_evaluation_data:
        expect_evaluation_text += evaluation.get("content", "") + " "

    # 기대평 (boardNo: 10)
    review_evaluation_url = f"{base_url}?best=false&notice=false&page=1&pageSize=40&sort=DESC_WRITE_DATE&boardNo=10&goodsCode={goods_code}"
    review_evaluation_response = requests.get(review_evaluation_url)

    if review_evaluation_response.status_code != 200:
        raise HTTPException(status_code=review_evaluation_response.status_code,
                            detail="Failed to fetch review evaluations")

    review_evaluation_text = ""
    review_evaluation_data = review_evaluation_response.json().get("data", [])
    for evaluation in review_evaluation_data:
        review_evaluation_text += evaluation.get("content", "") + " "

    combined_evaluation_text = expect_evaluation_text + review_evaluation_text

    return combined_evaluation_text


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
