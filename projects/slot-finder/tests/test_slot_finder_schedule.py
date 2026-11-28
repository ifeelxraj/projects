import unittest

from slotfind.slot_finder_calendar_reader import Booking
from slotfind.slot_finder_schedule import prepare
from slotfind.slot_finder_time_ranges import Span


class PlanTests(unittest.TestCase):
    def test_retains_source_labels_and_nonblocking_resources(self):
        plan = prepare([Span(0, 90)], [Span(1, 2)], [Booking("B", Span(5, 10)), Booking("A", Span(0, 5), "free")],
                       after=1)
        self.assertEqual(plan.resources, ("A", "B"))
        self.assertEqual([b.resource for b in plan.blockers], [None, "B"])
        self.assertEqual(plan.gaps, (Span(0, 1), Span(3, 5), Span(11, 90)))

    def test_summary_counts_overlapping_bookings_and_work_only_once(self):
        import json
        from test_slot_finder_commands import run
        rc, out, _ = run("summary", "--window", "09:00-10:00", "--window", "09:30-11:00",
                         "--busy", "08:00-09:30", "--busy", "09:15-09:45", "--format", "json")
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out), {"work_minutes": 120, "busy_minutes": 45, "free_minutes": 75,
                                           "free_blocks": 1, "longest_free_minutes": 75})

    def test_capacity_matches_packed_slots_rather_than_dividing_free_minutes(self):
        import json
        from test_slot_finder_commands import run
        opts = ("--window", "09:01-10:01", "--duration", "20", "--step", "15")
        stats = json.loads(run("summary", *opts, "--format", "json")[1])
        packed = run("slots", *opts, "--non-overlap")[1].splitlines()
        self.assertEqual((stats["meeting_capacity"], len(packed)), (1, 1))
        self.assertEqual(run("summary", "--step", "5")[0], 2)

    def test_explanation_distinguishes_closed_hours_and_padded_conflicts(self):
        from test_slot_finder_commands import run
        import json
        data = "resource,start,end\nBench,10:00,10:20"
        rc, out, _ = run("explain", "09:50-10:00", "--before", "5", "--calendar", "-", "--format", "json", text=data)
        info = json.loads(out)
        self.assertEqual((rc, info["inside_work"], info["available"]), (0, True, False))
        self.assertEqual(info["conflicts"], [{"resource": "Bench", "blocked": "09:55-10:20", "overlap": "09:55-10:00"}])
        self.assertIn("Not wholly inside", run("explain", "08:30-09:30")[1])

    def test_rooms_require_the_same_resource_for_the_entire_request(self):
        from test_slot_finder_commands import run
        data = "resource,start,end,status\nA,09:00,09:15,busy\nB,09:15,09:30,busy\nC,09:00,09:30,free"
        cmd = ("rooms", "09:00-09:30", "--calendar", "-")
        self.assertEqual(run(*cmd, text=data)[1], "C\n")
        self.assertEqual(run(*cmd, "--busy", "09:15-09:20", text=data)[1], "")
        self.assertEqual(run(*cmd, "--window", "10:00-12:00", text=data)[1], "")

    def test_resource_and_group_answers_match_independent_minute_sets(self):
        import random
        rng = random.Random(453)
        work = Span(5, 55)
        for _ in range(120):
            names = ("A", "B", "C")
            entries = [Booking(n, Span(*sorted(rng.sample(range(61), 2))),
                               rng.choice(["busy", "tentative", "free"])) for n in names]
            manual = Span(*sorted(rng.sample(range(61), 2)))
            query = Span(*sorted(rng.sample(range(61), 2)))
            before, after = rng.randrange(5), rng.randrange(4)
            ignore = rng.choice([True, False])
            plan = prepare([work], [manual], entries, before=before, after=after, ignore_tentative=ignore)
            needed = set(range(query.start, query.end))
            expected = []
            for event in entries:
                occupied = set(range(manual.start - before, manual.end + after))
                if event.status == "busy" or (event.status == "tentative" and not ignore):
                    occupied.update(range(event.interval.start - before, event.interval.end + after))
                if needed.issubset(range(work.start, work.end)) and needed.isdisjoint(occupied):
                    expected.append(event.resource)
            self.assertEqual(plan.available_resources(query), expected)
            self.assertEqual(plan.explain(query)["available"], len(expected) == len(names))
