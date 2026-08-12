

# from fastapi import APIRouter
# from app.models.complaint_model import BulkComplaintRequest, ComplaintRequest
# from app.services.ai_pipeline import process_complaint

# router = APIRouter()

# @router.post("/analyze-complaint")
# def analyze_complaint(data: ComplaintRequest):

#     result = process_complaint(
#         complaint=data.complaint,
#         address=data.address
#     )

#     return result

# @router.post("/analyze-bulk")
# def analyze_bulk(data: BulkComplaintRequest):

#     results = []

#     for item in data.complaints:
#         result = process_complaint(item.complaint, item.address)
#         results.append(result)

#     return results


from fastapi import APIRouter
from app.models.complaint_model import BulkComplaintRequest, ComplaintRequest
from app.services.ai_pipeline import process_complaint

router = APIRouter()

# @router.post("/analyze-complaint")
# def analyze_complaint(data: ComplaintRequest):
#     return process_complaint(data.complaint, data.address)

@router.post("/analyze-complaint")
def analyze_complaint(data: ComplaintRequest):

    result = process_complaint(data.complaint, data.address)

    return result
# @router.post("/analyze-complaint")
# def analyze_complaint(data: ComplaintRequest):

#     result = process_complaint(data.complaint, data.address)

#     return {
#         "id": "cmp_" + str(hash(data.complaint)),
#         "object": "complaint.analysis",
#         "created": 1710000000,

#         "result": result,

#         "meta": {
#             "model": "drug-ai-v2",
#             "language": "multilingual"
#         }
#     }


@router.post("/analyze-bulk")
def analyze_bulk(data: BulkComplaintRequest):

    results = []

    for item in data.complaints:
        result = process_complaint(item.complaint, item.address)
        results.append(result)

    return results