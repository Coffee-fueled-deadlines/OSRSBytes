from OSRSBytes import Hiscores


def test(verbose=True):
    pvp_user = Hiscores("C Engineer")
    boss_user = Hiscores("Hess")
    failed_tests = []

    for skill in boss_user.getSkillsGenerator():
        try:
            assert boss_user.skill(skill, "rank"), "Failed"
            # Assert that value, when converted to Int, is Int
            assert type(int(boss_user.skill(skill, "rank"))) == int, "Failed"
            assert boss_user.skill(skill, "level"), "Failed"
            # Assert that value, when converted to Int, is Int
            assert type(int(boss_user.skill(skill, "level"))) == int, "Failed"
            # Assert that value, when converted to Int, is Int
            assert type(int(boss_user.skill(skill, "experience"))) == int, "Failed"
        except:
            failed_tests.append(skill)
        if (verbose):
            print("Skill: {}\n\tRank: {}\n\tLevel: {}"
                .format(skill, boss_user.skill(skill,"rank"), boss_user.skill(skill,"level")))

    for activity in pvp_user.getPVPGenerator():
        try:
            assert pvp_user.lms_arena_sw(activity, "rank"), "Failed"
            assert pvp_user.lms_arena_sw(activity, "score"), "Failed"
        except:
            failed_tests.append(activity)
        if (verbose):
            print("Activity: {}\n\tRank: {}\n\tScore: {}"
                .format(activity, pvp_user.lms_arena_sw(activity,"rank"), pvp_user.lms_arena_sw(activity,"score")))

    for clue in boss_user.getClueGenerator():
        try:
            assert boss_user.clue(clue, "rank"), "Failed"
            assert boss_user.clue(clue, "score"), "Failed"
        except:
            failed_tests.append(clue)
        if (verbose):
            print("Clue Tier: {}\n\tRank: {}\n\tScore: {}"
                .format(clue, boss_user.clue(clue, "rank"), boss_user.clue(clue, "score")))

    for bounty in pvp_user.getBountyGenerator():
        try:
            assert pvp_user.bounty(bounty, "rank"), "Failed"
            assert pvp_user.bounty(bounty, "score"), "Failed"
        except:
            failed_tests.append(bounty)
        if (verbose):
            print("Bounty Type: {}\n\tRank: {}\n\tScore: {}"
                .format(bounty, pvp_user.bounty(bounty, "rank"), pvp_user.bounty(bounty, "score")))

    for boss in boss_user.getBossGenerator():
        try:
            assert boss_user.boss(boss, "rank"), "Failed"
            assert boss_user.boss(boss, "score"), "Failed"
        except:
            failed_tests.append(boss)
        if (verbose):
            print("Boss Name: {}\n\tRank: {}\n\tScore: {}"
                .format(boss, boss_user.boss(boss, "rank"), boss_user.boss(boss, "score")))

    assert len(failed_tests) == 0
    if (verbose):
        if len(failed_tests) == 0:
            print("\nTest Passed!")
            return True
        else:
            print("\nTest Failed!")
            print("\n\tNumber of Fails: {}".format(len(failed_tests)))
            print("\nTests that failed:")
            for fail in failed_tests:
                print("\t\t{}".format(fail))
            return False
    else:
        if len(failed_tests) == 0:
            return True
        else:
            return False
