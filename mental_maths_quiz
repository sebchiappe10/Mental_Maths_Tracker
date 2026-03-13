import time
import random
import threading
from datetime import datetime

from rich.console import Console
from rich.live import Live
from rich.text import Text
from rich.panel import Panel
from rich.table import Table


from csv_writers import write_question, write_session
from questions import generate_question

def generate_session_id():
    return datetime.now().strftime("%Y-%m-%d-%H%M%S")

console = Console()

OPERATORS = ["addition", "subtraction", "multiplication", "division", "percentage"]

OPERATOR_SYMBOLS = {
    "addition":       "+",
    "subtraction":    "−",
    "multiplication": "×",
    "division":       "/",
    "percentage":     "% of",
}

SESSION_DURATION = 120  # seconds


def run_session(level: int) -> None:


    while True:  # outer loop allows "play again" without full recursion

        # ------------------------------------------------------------------ #
        # 1. Session setup                                                     #
        # ------------------------------------------------------------------ #
        session_id   = generate_session_id()
        session_date = datetime.now().strftime("%Y-%m-%d")

        console.print(f"\n[bold cyan]Session ID:[/bold cyan] {session_id}")
        console.print(f"[bold]Level:[/bold] {level}  |  [bold]Duration:[/bold] {SESSION_DURATION}s\n")

        # 3-second countdown before the timer starts
        for i in range(3, 0, -1):
            console.print(f"[bold yellow]Starting in {i}…[/bold yellow]")
            time.sleep(1)
        console.print("[bold green]GO![/bold green]\n")

        # ------------------------------------------------------------------ #
        # 2. Shared timer state                                                #
        # ------------------------------------------------------------------ #
        start_time   = time.monotonic()
        timer_expired = threading.Event()   # set when time is up

        def _watch_timer() -> None:
            """Background thread: sets timer_expired after SESSION_DURATION."""
            time.sleep(SESSION_DURATION)
            timer_expired.set()

        timer_thread = threading.Thread(target=_watch_timer, daemon=True)
        timer_thread.start()

        # ------------------------------------------------------------------ #
        # 3. Question loop                                                     #
        # ------------------------------------------------------------------ #
        questions_log: list[dict] = []   # rows waiting to be written
        incorrect:     list[dict] = []   # kept for end-of-session display
        prev_operator: str | None = None
        q_number = 0

        while not timer_expired.is_set():

            # ── Operator selection (no two consecutive the same) ──────────── #
            available = [op for op in OPERATORS if op != prev_operator]
            operator  = random.choice(available)
            prev_operator = operator

            # ── Generate question ─────────────────────────────────────────── #
            q        = generate_question(operator, level)
            symbol   = OPERATOR_SYMBOLS[operator]
            q_number += 1

            # Format: "12 + 7 = ?" or "25 % of 80 = ?"
            if operator == "percentage":
                question_str = f"[bold]{q['number_1']}% of {q['number_2']}[/bold] = ?"
            else:
                question_str = f"[bold]{q['number_1']} {symbol} {q['number_2']}[/bold] = ?"

            # ── Display question with live countdown ──────────────────────── #
            console.print(f"\n[dim]Q{q_number}[/dim]  {question_str}")

            q_start_ms = time.monotonic()

            # ── Input loop: accept only valid numeric input ───────────────── #
            user_answer = None
            while user_answer is None:
                # Check timer before blocking on input
                if timer_expired.is_set():
                    break

                elapsed   = time.monotonic() - start_time
                remaining = max(0, SESSION_DURATION - elapsed)

                # Show remaining time as a prompt prefix
                try:
                    raw = console.input(
                        f"[dim][{remaining:05.1f}s][/dim] Your answer: "
                    ).strip()
                except EOFError:
                    # Handle piped input / non-interactive environments
                    timer_expired.set()
                    break

                # Validate: must be a number (int or float)
                try:
                    user_answer = float(raw)
                except ValueError:
                    # Invalid input — wait silently for a valid answer
                    continue

            # ── Timer expired while waiting for input — end session ────────── #
            if timer_expired.is_set() and user_answer is None:
                console.print("\n[bold red]⏰  Time's up![/bold red]")
                break

            # ── Timer expired the moment an answer was submitted ─────────── #
            # (answered after the buzzer — discard this question)
            if timer_expired.is_set():
                console.print("[dim]Answer submitted after time expired — not counted.[/dim]")
                break

            # ── Evaluate answer ───────────────────────────────────────────── #
            response_time_ms = round((time.monotonic() - q_start_ms) * 1000)

            correct_rounded = round(q["correct_answer"], 2)
            user_rounded    = round(user_answer, 2)
            is_correct      = correct_rounded == user_rounded

            if is_correct:
                console.print("[green]✓  Correct![/green]")
            else:
                console.print(
                    f"[red]✗  Incorrect.[/red]  "
                    f"Answer was [bold]{correct_rounded}[/bold]"
                )

            # ── Build the row dict for questions.csv ──────────────────────── #
            row = {
                "session_id":      session_id,
                "date":            session_date,
                "operator":        operator,
                "number_1":        q["number_1"],
                "number_2":        q["number_2"],
                "correct_answer":  correct_rounded,
                "my_answer":       user_rounded,
                "is_correct":      is_correct,
                "response_time_ms": response_time_ms,
                "difficulty_level": level,
            }

            write_question(row)
            questions_log.append(row)

            if not is_correct:
                incorrect.append(row)

        # ------------------------------------------------------------------ #
        # 4. Session end                                                       #
        # ------------------------------------------------------------------ #
        total   = len(questions_log)
        correct = sum(1 for r in questions_log if r["is_correct"])
        pct     = round((correct / total * 100), 1) if total > 0 else 0.0

        # Operator breakdown for the summary (comma-separated unique operators used)
        operators_used = list(dict.fromkeys(r["operator"] for r in questions_log))
        operator_focus = ", ".join(operators_used) if operators_used else "none"

        summary = {
            "session_id":       session_id,
            "date":             session_date,
            "level":            level,
            "total_questions":  total,
            "correct":          correct,
            "score_percent":    pct,
            "operator_focus":   operator_focus,
        }

        write_session(summary)

        # ── Score panel ───────────────────────────────────────────────────── #
        console.print()
        score_color = "green" if pct >= 80 else "yellow" if pct >= 50 else "red"
        console.print(Panel(
            f"[bold]Questions:[/bold] {total}   "
            f"[bold]Correct:[/bold] {correct}   "
            f"[{score_color}][bold]Score: {pct}%[/bold][/{score_color}]",
            title="[bold]Session Complete[/bold]",
            expand=False,
        ))

        # ── Incorrect questions table ─────────────────────────────────────── #
        if incorrect:
            table = Table(title="Questions to Review", show_lines=True)
            table.add_column("Question",       style="cyan")
            table.add_column("Your Answer",    style="red")
            table.add_column("Correct Answer", style="green")

            for r in incorrect:
                sym = OPERATOR_SYMBOLS[r["operator"]]
                if r["operator"] == "percentage":
                    q_str = f"{r['number_1']}% of {r['number_2']}"
                else:
                    q_str = f"{r['number_1']} {sym} {r['number_2']}"

                table.add_row(q_str, str(r["my_answer"]), str(r["correct_answer"]))

            console.print(table)

        # ── Play again? ───────────────────────────────────────────────────── #
        console.print()
        again = console.input("[bold]Play again? (y/n):[/bold] ").strip().lower()

        if again == "y":
            console.print()
            continue          # restart the outer while loop (new session ID)
        else:
            console.print("[bold cyan]Thanks for playing. Goodbye![/bold cyan]")
            break             # exit cleanly

