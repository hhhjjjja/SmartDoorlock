# DeepLearning Project
Jetson Nano와 영상처리 기반의 스마트 도어락 제작 프로젝트

## 개발환경
- Jetson Nano
- Linux Ubuntu
- Pytorch
- Python 3.6

## 제작 과정
- 제작 기간
  - 총 제작기간 : 2020. 07. 31 ~ 2020. 08. 04
  
  - 기획 및 설계 : 2020. 07. 31 (1일)
  - 개발 : 2020. 08. 01 ~ 2020. 08. 04 (3일_8.2일 제외)
  - 데모데이 / 발표 : 2020. 08. 05
  
- 제작 인원
  - 박현정 : 설계, 이미지학습, 최적화
  - 정성윤 : 하드웨어 셋팅, 테스트
  
- 프로젝트 요약
  - Jetson Nano에 리눅스 우분투 개발환경 구축
  - Pytorch를 활용하여 이미지 학습
    - 이미지 트레이닝을 통한 손가락 모션 학습
  - Imagenet & network:resnet18 사용하여 이미지 Detecting
    - 초기 비밀번호 동작을 class_id 를 활용하여 설정
    - 인식된 모션에 따라 OLED, LED 출력
    - 인식된 모션의 class_id와 초기설정 class_id 비교 후 lock/unlock
    
  - 하드웨어 회로도
  <img src="https://user-images.githubusercontent.com/59678496/89259268-e9742c80-d664-11ea-80b8-217a8e8d68a9.png">
  
## 결과물
[ HardWare ]

<img src="https://user-images.githubusercontent.com/59678496/89260583-85069c80-d667-11ea-834b-bb9e9212669e.gif">

[ Ubuntu Image Detecting ]

<img src="https://user-images.githubusercontent.com/59678496/89260955-373e6400-d668-11ea-8389-4eafdc7edf3f.gif">
