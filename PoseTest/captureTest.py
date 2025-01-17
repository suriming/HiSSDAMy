import cv2
import mediapipe as mp
import PoseModule as poseModule
import time
import sys

# pose 돌리는데 필요한 모듈들을 변수에 담아줌
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 웹캠을 연결함
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# pose 돌리는 데 필요한 설정
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 캡쳐를 위한 변수
capture_count = 0
capture_coordinates = {}
# 타이머 시간 설정 (초)
end = 2
current_time = 1

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("EMPTY CAMERA FRAME")
        continue
    key = cv2.waitKey(1) & 0xFF
    image_height, image_width, _ = image.shape

    # 포즈 모듈 실행 함수 실행
    pose_results, output_image = poseModule.detectPose(image, pose)

    # 눈 좌우와 코의 x좌표값 구하기
    leftEyeInner = int(pose_results.pose_landmarks.landmark[1].x * image_width)
    rightEyeInner = int(pose_results.pose_landmarks.landmark[4].x * image_width)
    nose = int(pose_results.pose_landmarks.landmark[0].x * image_width)

    """캡쳐 타임~~!!!"""
    if key == ord('a'):
        # 파일 이름 구별을 위한 숫자 증가
        capture_count += 1
        # 좌표값 저장
        left_eye_x = leftEyeInner
        right_eye_x = rightEyeInner
        nose_x = nose
        print(left_eye_x, right_eye_x, nose_x)
        # 캡쳐된 사진에서의 왼쪽, 오른쪽 눈과 코 사이의 거리 구하기
        leftDist = abs(leftEyeInner - nose)
        rightDist = abs(rightEyeInner - nose)
        print(f'left: {leftDist}, right:{rightDist}')
        # 이미지 파일 저장 (이미 있으면 덮어쓰기 됨)
        image_file_name = 'capture' + str(capture_count) + '.png'
        cv2.imwrite(image_file_name, cv2.flip(image, 1))
        # 이미지 파일 별 좌표값 딕셔너리에 저장
        capture_coordinates[image_file_name] = {'left_eye_x': left_eye_x, 'right_eye_x': right_eye_x, 'nose_x': nose_x,
                                                'leftDist': leftDist, 'rightDist': rightDist}
    """ㄴ여기까지 함수로 묶기"""

    cv2.imshow('PoseModuleTest', output_image)
    if key == 27:
        break

cap.release()

print(f"----------------------------{capture_coordinates}-------------------------")


while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("EMPTY CAMERA FRAME")
        continue
    key = cv2.waitKey(1) & 0xFF
    image_height, image_width, _ = image.shape

    # 포즈 모듈 실행 함수 실행
    pose_results, output_image = poseModule.detectPose(image, pose)

    # 눈 좌우와 코의 x좌표값 구하기
    leftEyeInner = int(pose_results.pose_landmarks.landmark[1].x * image_width)
    rightEyeInner = int(pose_results.pose_landmarks.landmark[4].x * image_width)
    nose = int(pose_results.pose_landmarks.landmark[0].x * image_width)

    """더미데이터!!!!! @수림언니!! 여기다가 뭔가 딕셔너리 형태로 넣어주세용"""
    capture_item = {'capture1.png': '조명', 'capture2.png': 'TV', 'capture3.png': '에어컨'}

    """좌표값 비교"""
    # 왼쪽, 오른쪽 눈과 코 사이의 거리를 구하기
    leftDist = abs(leftEyeInner - nose)
    rightDist = abs(rightEyeInner - nose)
    centerDist = abs(rightDist - leftDist)
    current_time = time.time()

    # 시선 추적 버튼을 누르면 2초동안 판단하겠다
    current_time = time.time()
    if key == ord('b'):
        time_end = current_time + end
    if current_time >= time_end:
        if len(capture_item) == 3:
            for img_name, item_name in capture_item.items():
                leftDist_standard = capture_coordinates[img_name]['leftDist']
                rightDist_standard = capture_coordinates[img_name]['rightDist']
                if (leftDist_standard - 5 <= leftDist <= leftDist_standard + 5) and (
                        rightDist_standard - 5 <= rightDist <= rightDist_standard + 5):
                    detected_item = item_name
                else:
                    continue
        else:
            print("쓰담이 사물 설정을 완료해주세요")
            pass
        time_end = sys.maxsize
    else:
        pass

    cv2.imshow('PoseModuleTest', output_image)
    if key == 27:
        break

cap.release()




