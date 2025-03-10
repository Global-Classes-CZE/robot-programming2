from microbit import pin14, pin15, sleep, display
from utime import ticks_us, ticks_diff

if __name__ == "__main__":
    # init
    pocet_tikov_dict = {"prava": {"pocet_tikov": 0, "stav_predtym": 0}, "lava": {"pocet_tikov": 0, "stav_predtym": 0}}
    cas_minule = 0

    def pocet_tikov(strana, novy_stav):
        # Overenie ci sa stav zmenil
        if pocet_tikov_dict[strana]["stav_predtym"] != novy_stav:
            pocet_tikov_dict[strana]["stav_predtym"] = novy_stav
            pocet_tikov_dict[strana]["pocet_tikov"] += 1
        return pocet_tikov_dict[strana]["pocet_tikov"]

    cas_minule = ticks_us()
    while True:
        pocet_tikov_prava = pocet_tikov("prava", pin14.read_digital())
        pocet_tikov_lava = pocet_tikov("lava", pin15.read_digital())

        cas_teraz = ticks_us()
        if ticks_diff(cas_teraz, cas_minule) > 1000000:
            print(pocet_tikov_prava, " | ", pocet_tikov_lava)
            cas_minule = cas_teraz
        sleep(5)