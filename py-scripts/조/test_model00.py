'''
=====================[transformers 설치]=====================
Python 3.8 이상에서만 사용 가능

winget install -e --id Rustlang.Rustup
오류 발생시
[window powershell 관리자 권한 실행]
    winget source remove msstore
    winget source remove winget

    winget source add --name winget https://cdn.winget.microsoft.com/cache
    winget source add --name msstore https://storeedgefd.dsx.mp.microsoft.com/v9.0

    winget source update
    (PC재부팅 후) winget install -e --id Rustlang.Rustup

rustc --version
cargo --version

결과 안나오면
[Rust 환경변수 설정]
    1. cmd 창 입력 : sysdm.cpl
    2. 환경변수 Path 추가 : C: Users 사용자이름 .cargo bin
    3. --version 재확인

[MS C++ build tools 설치]
    https://visualstudio.microsoft.com/ko/visual-cpp-build-tools/
    위 사이트에서 build tools 다운로드
    설치파일 실행하고 개별구성요소에서 아래 옵션 선택 후 설치
        MSVC v143 - x64/x86 Build Tools
        Windows 10 SDK (10.0.19041.0 이상)
        C++ CMake tools for Windows
        Windows Universal CRT SDK
        C++ x64/x86 Spectre-mitigated lib
        C++ Clang Compiler for Windows
    설치 후 환경변수 등록(버전확인하고 입력해야 함)
        C: Program Files Microsoft Visual Studio 2022 BuildTools VC Tools MSVC 14.3x.xxxxx bin Hostx64 x64
        C: Program Files (x86) WindowsKits 10 bin 10.0.19041.0 x64
    환경변수 등록하고 PC 재부팅
    설치 확인 : terminal에 'cl' 입력

rustc, cargo --version 확인

rustup update
rustup default stable

setx PATH "%PATH%;C: Users 사용자이름 .cargo bin"

pip install --upgrade pip

pip install torch torchvision torchaudio

pip install transformers

conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia (오래걸림)

(추가 패키지)
pip install -U sentence-transformers
pip install tokenizers
=============================================================
'''

'''GPU를 사용하고 있는지 확인'''
import torch

# GPU가 사용 가능한지 확인
print("CUDA Available:", torch.cuda.is_available())

# GPU 정보 출력
if torch.cuda.is_available():
    print("GPU Name:", torch.cuda.get_device_name(0))
    print("CUDA Version:", torch.version.cuda)

'''라벨 체계 확인'''
from transformers import AutoConfig

# 사용한 감성 분석 모델 로드
model_name = "beomi/KcELECTRA-base"
config = AutoConfig.from_pretrained(model_name)

# 라벨 확인
print(config.id2label)


'''KoBERT & KcELECTRA 감성 분석을 GPU에서 실행'''
import torch
from transformers import pipeline

# GPU 사용 가능 여부 확인
device = 0 if torch.cuda.is_available() else -1
print(f"Using device: {'GPU' if device == 0 else 'CPU'}")

# KcELECTRA 감성 분석 모델 로드 (GPU 사용 설정)
classifier = pipeline("sentiment-analysis", model="beomi/KcELECTRA-base", device=device)

# 테스트 실행
result = classifier("이 주식은 망할 것 같다.")
print(result)
