import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from playwright.sync_api import sync_playwright, expect

APP_URL = "file:///" + str(Path(__file__).parent / "index.html").replace("\\", "/")
SCREENSHOT_DIR = Path(__file__).parent / "test_screenshots"
SCREENSHOT_DIR.mkdir(exist_ok=True)

results = []

def ok(name, detail=""):
    results.append(("PASS", name, detail))
    print(f"  ✅ {name}" + (f" — {detail}" if detail else ""))

def fail(name, detail=""):
    results.append(("FAIL", name, detail))
    print(f"  ❌ {name}" + (f" — {detail}" if detail else ""))

def shot(page, name):
    path = SCREENSHOT_DIR / f"{name}.png"
    page.screenshot(path=str(path))
    return path

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(viewport={"width": 520, "height": 750})
        page = ctx.new_page()

        page.goto(APP_URL)
        page.evaluate("localStorage.clear()")
        page.reload()

        print("\n[1] 초기 상태")
        empty = page.locator(".empty")
        if empty.is_visible():
            ok("빈 상태 메시지 표시")
        else:
            fail("빈 상태 메시지 미표시")
        shot(page, "01_initial")

        print("\n[2] 아이템 추가 — 버튼 클릭")
        page.locator("#input").fill("사과")
        page.locator("button[title='추가']").click()
        items = page.locator(".item")
        count = items.count()
        if count == 1 and "사과" in items.first.inner_text():
            ok("버튼으로 아이템 추가", "사과 추가됨")
        else:
            fail("버튼으로 아이템 추가", f"count={count}")
        shot(page, "02_add_button")

        print("\n[3] 아이템 추가 — Enter 키")
        page.locator("#input").fill("바나나")
        page.locator("#input").press("Enter")
        count = page.locator(".item").count()
        if count == 2:
            ok("Enter 키로 아이템 추가", "바나나 추가됨")
        else:
            fail("Enter 키로 아이템 추가", f"count={count}")

        page.locator("#input").fill("우유")
        page.locator("#input").press("Enter")
        shot(page, "03_three_items")

        print("\n[4] 입력창 자동 초기화")
        val = page.locator("#input").input_value()
        if val == "":
            ok("추가 후 입력창 비워짐")
        else:
            fail("추가 후 입력창 비워짐", f"남은 값='{val}'")

        print("\n[5] 헤더 통계 업데이트")
        stats = page.locator("#stats").inner_text()
        if "3" in stats:
            ok("헤더 통계 표시", stats)
        else:
            fail("헤더 통계 표시", stats)

        print("\n[6] 아이템 체크")
        first_cb = page.locator(".item input[type='checkbox']").first
        first_cb.check()
        first_item = page.locator(".item").first
        cls = first_item.get_attribute("class") or ""
        if "done" in cls:
            ok("체크 시 done 클래스 적용")
        else:
            fail("체크 시 done 클래스 적용", f"class='{cls}'")

        text_deco = first_item.locator(".item-text").evaluate(
            "el => getComputedStyle(el).textDecorationLine"
        )
        if "line-through" in text_deco:
            ok("체크된 항목에 취소선 표시")
        else:
            fail("체크된 항목에 취소선 표시", f"decoration='{text_deco}'")
        shot(page, "06_checked")

        print("\n[7] 완료 카운터 업데이트")
        done_text = page.locator("#done-count").inner_text()
        if "1" in done_text and "3" in done_text:
            ok("완료 카운터 업데이트", done_text)
        else:
            fail("완료 카운터 업데이트", done_text)

        print("\n[8] 아이템 체크 해제 (토글)")
        first_cb.uncheck()
        cls = page.locator(".item").first.get_attribute("class") or ""
        if "done" not in cls:
            ok("체크 해제 (토글)")
        else:
            fail("체크 해제 (토글)", f"class='{cls}'")

        print("\n[9] 아이템 삭제")
        before = page.locator(".item").count()
        page.locator(".delete-btn").first.click()
        after = page.locator(".item").count()
        if after == before - 1:
            ok("삭제 버튼으로 아이템 제거", f"{before} → {after}개")
        else:
            fail("삭제 버튼으로 아이템 제거", f"before={before}, after={after}")
        shot(page, "09_deleted")

        print("\n[10] 완료 항목 일괄 삭제")
        page.locator(".item input[type='checkbox']").first.check()
        checked_before = page.locator(".item.done").count()
        page.locator(".clear-btn").click()
        remaining = page.locator(".item").count()
        if remaining == page.locator(".item").count() and page.locator(".item.done").count() == 0:
            ok("완료 항목 일괄 삭제", f"체크된 {checked_before}개 삭제됨")
        else:
            fail("완료 항목 일괄 삭제")
        shot(page, "10_clear_done")

        print("\n[11] localStorage 데이터 유지")
        page.locator("#input").fill("새우깡")
        page.locator("#input").press("Enter")
        before_reload = page.locator(".item").count()
        page.reload()
        after_reload = page.locator(".item").count()
        if after_reload == before_reload:
            ok("새로고침 후 데이터 유지", f"{after_reload}개 유지됨")
        else:
            fail("새로고침 후 데이터 유지", f"before={before_reload}, after={after_reload}")
        shot(page, "11_after_reload")

        print("\n[12] 🔍 경계값 — 공백만 입력")
        count_before = page.locator(".item").count()
        page.locator("#input").fill("   ")
        page.locator("#input").press("Enter")
        count_after = page.locator(".item").count()
        if count_after == count_before:
            ok("🔍 공백 입력 무시됨")
        else:
            fail("🔍 공백 입력 무시됨", "공백 항목이 추가됨")

        print("\n[13] 🔍 경계값 — 빈 입력")
        count_before = page.locator(".item").count()
        page.locator("#input").fill("")
        page.locator("button[title='추가']").click()
        count_after = page.locator(".item").count()
        if count_after == count_before:
            ok("🔍 빈 입력 무시됨")
        else:
            fail("🔍 빈 입력 무시됨", "빈 항목이 추가됨")

        print("\n[14] 🔍 경계값 — XSS 특수문자 입력")
        xss = '<script>alert("xss")</script>'
        page.locator("#input").fill(xss)
        page.locator("#input").press("Enter")
        items_html = page.locator(".list").inner_html()
        if "<script>" not in items_html:
            ok("🔍 XSS 이스케이프 처리됨")
        else:
            fail("🔍 XSS 이스케이프 처리됨", "스크립트 태그가 그대로 삽입됨")
        shot(page, "14_xss_probe")

        print("\n[15] 🔍 모두 삭제 후 빈 상태 복귀")
        for _ in range(page.locator(".item").count()):
            page.locator(".delete-btn").first.click()
        empty_visible = page.locator(".empty").is_visible()
        if empty_visible:
            ok("🔍 모두 삭제 후 빈 상태 메시지 복귀")
        else:
            fail("🔍 모두 삭제 후 빈 상태 메시지 복귀")
        shot(page, "15_empty_again")

        browser.close()

    print("\n" + "="*50)
    passed = sum(1 for r in results if r[0] == "PASS")
    failed = sum(1 for r in results if r[0] == "FAIL")
    print(f"결과: {passed} 통과 / {failed} 실패 / 총 {len(results)}개")
    if failed:
        print("\n실패 목록:")
        for r in results:
            if r[0] == "FAIL":
                print(f"  ❌ {r[1]}" + (f" ({r[2]})" if r[2] else ""))
    return failed == 0

if __name__ == "__main__":
    print(f"앱 경로: {APP_URL}")
    print(f"스크린샷: {SCREENSHOT_DIR}")
    success = run_tests()
    sys.exit(0 if success else 1)
