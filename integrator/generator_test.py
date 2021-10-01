from sortedcontainers import SortedDict, SortedSet, SortedSet  # type: ignore
from model import Index, Usage, Counter
from generator import _get_dict_counts


def test__get_dict_counts():
    d = SortedDict(
        {
            "ὑπερβλύω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερβλύζων", "прѣ\ue205сто\ue20dе",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        key=(
                                            "ὑπερβλύζων",
                                            "прѣ\ue205сто\ue20dе",
                                        ),
                                    ),
                                    lang="gr",
                                    var="C",
                                    orig_alt="ὑπερκλύζω",
                                    orig_alt_var={},
                                    trans_alt="",
                                    trans_alt_var={},
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερβλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        key=(
                                            "ὑπερβλύσαι",
                                            "\ue205сто\ue20dен\ue205\ue205",
                                        ),
                                    ),
                                    lang="gr",
                                    var="C",
                                    orig_alt="ὑπερκλύζω",
                                    orig_alt_var={},
                                    trans_alt="",
                                    trans_alt_var={},
                                )
                            ]
                        )
                    },
                }
            ),
            "ὑπερκλύζω": SortedDict(
                {
                    "прѣ\ue205сто\ue20d\ue205т\ue205": {
                        ("ὑπερκλύζων", "прѣ\ue205сто\ue20dе",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        key=(
                                            "ὑπερκλύζων",
                                            "прѣ\ue205сто\ue20dе",
                                        ),
                                    ),
                                    lang="gr",
                                    var="",
                                    orig_alt="",
                                    orig_alt_var={"C": "ὑπερβλύω"},
                                    trans_alt="",
                                    trans_alt_var={},
                                )
                            ]
                        )
                    },
                    "\ue205сто\ue20dен\ue205\ue201": {
                        ("ὑπερκλύσαι", "\ue205сто\ue20dен\ue205\ue205",): SortedSet(
                            [
                                Usage(
                                    idx=Index(
                                        ch=1,
                                        alt=True,
                                        page=168,
                                        col="c",
                                        row=17,
                                        key=(
                                            "ὑπερκλύσαι",
                                            "\ue205сто\ue20dен\ue205\ue205",
                                        ),
                                    ),
                                    lang="gr",
                                    var="",
                                    orig_alt="",
                                    orig_alt_var={"C": "ὑπερβλύω"},
                                    trans_alt="",
                                    trans_alt_var={},
                                )
                            ]
                        )
                    },
                }
            ),
        }
    )
