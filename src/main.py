"""
Implement User Management System
"""
import datetime

# 초기 사용자 목록
users = {
    "intel": {
        "name": "관리자",
        "birth": "19800101",
        "password": "sesacintelai",
        "role": "admin"
    },
    "dooroo": {
        "name": "편집자",
        "birth": "19920101",
        "password": "dooroodooroo",
        "role": "editor"
    },
    "blistex": {
        "name": "조회자",
        "birth": "20000101",
        "password": "iamjustaviewer",
        "role": "viewer"
    }
}

def print_users():
    print("\n전체 사용자 목록:")
    for user_id, info in users.items():
        print(f"\nID: {user_id}")
        print(f"이름: {info['name']}")
        print(f"생년월일: {info['birth']}")
        print(f"역할: {info['role']}")
    print()


def is_valid_date(dob_str):
    try:
        datetime.datetime.strptime(dob_str, "%Y%m%d")
        return True
    except ValueError:
        return False


def is_valid_role(role):
    return role in {"viewer", "editor", "admin"}


def add_user():
    print("\n새 사용자 추가")

    while True:
        user_id = input("아이디를 입력하세요: ")
        if user_id in users:
            print("이미 존재하는 아이디입니다.")
        else:
            break

    name = input("이름을 입력하세요: ")

    while True:
        birth = input("생년월일을 입력하세요 (YYYYMMDD): ")
        if is_valid_date(birth):
            break
        else:
            print("유효하지 않은 날짜입니다.")

    while True:
        password = input("비밀번호를 입력하세요 (10자 이상): ")
        if len(password) >= 10:
            break
        else:
            print("비밀번호는 10자 이상이어야 합니다.")

    while True:
        role = input("역할을 입력하세요 (viewer/editor/admin): ").lower()
        if is_valid_role(role):
            break
        else:
            print("역할은 viewer, editor, admin 중 하나여야 합니다.")

    users[user_id] = {
        "name": name,
        "birth": birth,
        "password": password,
        "role": role
    }

    print(f"\n사용자 '{user_id}' 추가 완료!")
    print_users()


def modify_user(logged_in_id, role):
    print("\n사용자 정보 수정")
    if role in ["editor", "admin"]:
        target_id = input("수정할 사용자 ID를 입력하세요: ")
    else:
        target_id = logged_in_id

    if target_id not in users:
        print("해당 사용자가 존재하지 않습니다.")
        return

    print(f"현재 정보: {users[target_id]}")
    name = input("새 이름 (Enter로 건너뛰기): ") or users[target_id]['name']
    birth = input("새 생년월일 (YYYYMMDD, Enter로 건너뛰기): ") or users[target_id]['birth']
    if birth and not is_valid_date(birth):
        print("유효하지 않은 생년월일입니다.")
        return
    password = input("새 비밀번호 (10자 이상, Enter로 건너뛰기): ")
    if password and len(password) < 10:
        print("비밀번호는 10자 이상이어야 합니다.")
        return

    users[target_id]['name'] = name
    users[target_id]['birth'] = birth
    if password:
        users[target_id]['password'] = password

    print(f"\n사용자 '{target_id}' 정보 수정 완료!")
    print_users()


def delete_user(logged_in_id, role):
    print("\n사용자 삭제")

    if role == "admin":
        target_id = input("삭제할 사용자 ID를 입력하세요: ")
    else:
        target_id = logged_in_id

    if target_id not in users:
        print("해당 사용자가 존재하지 않습니다.")
        return

    if target_id == logged_in_id or role == "admin":
        del users[target_id]
        print(f"사용자 '{target_id}' 삭제 완료!")
        print_users()
        if target_id == logged_in_id:
            print("본인 계정을 삭제하여 로그아웃됩니다.")
            return False  # 본인 삭제 시 로그아웃
    else:
        print("삭제 권한이 없습니다.")

    return True


def login():
    print("\n로그인")
    user_id = input("아이디: ")
    password = input("비밀번호: ")

    if user_id in users and users[user_id]['password'] == password:
        print(f"\n로그인 성공! '{user_id}' ({users[user_id]['role']})")
        return user_id
    else:
        print("로그인 실패: 아이디 또는 비밀번호 오류")
        return None


def user_menu(user_id):
    role = users[user_id]['role']
    while True:
        print(f"\n사용자 메뉴 - 권한: {role}")
        print("1. 내 정보 수정")
        print("2. 사용자 정보 수정")
        print("3. 사용자 삭제")
        if role == "admin":
            print("4. 새 사용자 추가")
        print("0. 로그아웃")

        choice = input("선택: ")

        if choice == "1":
            modify_user(user_id, "viewer")
        elif choice == "2":
            if role in ["editor", "admin"]:
                modify_user(user_id, role)
            else:
                print("권한이 없습니다.")
        elif choice == "3":
            keep_logged_in = delete_user(user_id, role)
            if not keep_logged_in:
                break
        elif choice == "4" and role == "admin":
            add_user()
        elif choice == "0":
            print("로그아웃합니다.")
            break
        else:
            print("올바른 메뉴를 선택하세요.")


def main():
    print_users()
    while True:
        print("\n===== 로그인 시스템 =====")
        print("1. 로그인")
        print("0. 종료")
        choice = input("선택: ")

        if choice == "1":
            user_id = login()
            if user_id:
                user_menu(user_id)
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다.")


main()
