# Main Section
from app.services.utils.utils import char_recognizer, ocr_result_processor, get_model, info_extraction, correct_seat_info
import time # for test

class InfoExtraction:
    """
    티켓 이미지로부터 정보 추출
    input_img: 입력 이미지
    model: 정보 추출에 사용될 모델(Gemini)
    """
    def __init__(self, input_img):
        self.input_img = input_img
        self.model = get_model()

    def info_extractor(self):
        """
        char_recognizer: OCR
        ocr_result_processor: OCR 결과 처리
        info_extraction: 정보 추출
        correct_seat_info: 좌석정보 정제
        """
        ticket_words = char_recognizer(self.input_img)
        ticket_info_processed = ocr_result_processor(ticket_words)
        infos = info_extraction(ticket_info_processed, self.model)
        try:
            corrected_seat_info = correct_seat_info(infos)
            infos['좌석정보'] = corrected_seat_info
        except:
            try:
                # Exception1: 부적합한 결과가 드물게 발생 => 다시 수행
                infos = info_extraction(ticket_info_processed)
                corrected_seat_info = correct_seat_info(infos)
                infos['좌석정보'] = corrected_seat_info
            except:
                # Exception2: 정보 없음으로 처리
                pass
        return infos


class OcrService:
    def run_ocr(self):
        self.other_function()
        ##### test #####
        start_time = time.time()
        ticket_infos = InfoExtraction('/Users/art029/PycharmProjects/ticats_ai_server/app/services/utils/s27.jpg').info_extractor()
        end_time = time.time()
        execution_time = end_time - start_time

        print(ticket_infos)
        print(f"Execution time: {execution_time} secs")
        ##### test #####
        #return "hello"

    def other_function(self):
        pass
