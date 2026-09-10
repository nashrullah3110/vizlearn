# -*- coding: utf-8 -*-
"""Every named-architecture module, from the three per-track content files.

Fifteen modules about models that have names - VGG-16, Inception, ResNet,
U-Net, YOLO v8, Mask R-CNN, Haar cascades, word2vec, GloVe, seq2seq, neural
machine translation, GANs, autoencoders, collaborative filtering, neural
recommenders - built by tools/build_arch_topics.py and driven by one shared
harness in assets/vizlearn-arch.js.

The content lives in arch_cv.py, arch_nlp.py and arch_dl.py. This module only
concatenates them and exposes the three derived dictionaries the rest of the
build reads: questions for tools/labs.py, citations for tools/references.py,
and meta descriptions for tools/descriptions.py. Keeping those derivations
here rather than repeating them in each consumer means a new module is one
edit in one content file.
"""

from arch_cv import TOPICS as _CV
from arch_nlp import TOPICS as _NLP
from arch_dl import TOPICS as _DL

TOPICS = _CV + _NLP + _DL


def _path(t):
    return "%s/%s.html" % (t["dir"], t["slug"])


# tools/labs.py merges this, so a question written against the exact explorer
# on the page lives beside it rather than in a second file that can drift.
CHECKS = {_path(t): {"check": t["check"]} for t in TOPICS}

# tools/references.py merges this. Pages with nothing genuine to cite get no
# section at all rather than a filler link, which is the rule that file states.
REFERENCES = {_path(t): t["refs"] for t in TOPICS if t["refs"]}

# tools/descriptions.py merges this. The meta description is what a search
# result and a social card show, so it says what the reader will actually do
# on the page rather than what the page is about.
DESCRIPTIONS = {_path(t): t["description"] for t in TOPICS if t["description"]}

# Where each generated module slots into its track, as (anchor, [new pages]).
# tools/sequence.py splices these in, so the ordering lives beside the content
# that determines it: Haar cascades after the classical detectors that share
# their assumptions, the backbones after transfer learning because that is
# what a backbone is for, the detectors after IoU and NMS because they cannot
# be read without them.
#
# Expressing it as "after this existing page" rather than as an absolute index
# means reordering a track by hand does not silently move these somewhere
# nonsensical.
INSERT_AFTER = {
    "computer-vision": [
        ("computer_vision/harris_corners.html",
         ["computer_vision/haar_cascade_detection.html"]),
        ("computer_vision/transfer_learning_with_cnn.html",
         ["computer_vision/vgg16_architecture.html",
          "computer_vision/inception_architecture.html"]),
        ("computer_vision/object_detection_with_bounding_boxes.html",
         ["computer_vision/yolov8_detection.html"]),
        ("computer_vision/resnet_and_identity_shortcuts.html",
         ["computer_vision/resnet_architecture.html"]),
        ("computer_vision/semantic_segmentation_unet.html",
         ["computer_vision/unet_architecture.html",
          "computer_vision/mask_rcnn.html"]),
    ],
    "nlp": [
        ("natural_language_processing/how_are_embeddings_generated.html",
         ["natural_language_processing/word2vec.html",
          "natural_language_processing/glove.html"]),
        ("natural_language_processing/what_is_bi_directional_layer.html",
         ["natural_language_processing/seq2seq_architecture.html"]),
        ("natural_language_processing/attention_mechanism.html",
         ["natural_language_processing/machine_translation_encoder_decoder.html"]),
    ],
    "dl": [
        ("deep_learning/autoencoders.html",
         ["deep_learning/autoencoders_conceptual_and_pytorch.html"]),
        ("deep_learning/generative_adversarial_networks.html",
         ["deep_learning/gan_architecture.html"]),
        ("deep_learning/seq2seq_and_beam_search.html",
         ["deep_learning/collaborative_filtering.html",
          "deep_learning/deep_learning_for_recommendation_systems.html"]),
    ],
}


def splice(track, paths):
    """`paths` with this track's generated modules inserted after their anchors.

    Raises rather than appending silently if an anchor has gone: an anchor
    that no longer exists means somebody renamed a page, and quietly dropping
    four modules to the end of the track is not the behaviour that helps them
    notice.
    """
    out = list(paths)
    for anchor, added in INSERT_AFTER.get(track, []):
        if anchor not in out:
            raise SystemExit(
                "arch_topics: anchor %s is not in the %s sequence" % (anchor, track))
        at = out.index(anchor) + 1
        out[at:at] = [p for p in added if p not in out]
    return out


def _check_order():
    """Every generated page must be spliced into exactly one track.

    apply_sequence.py drops anything courseData holds that sequence.py does
    not list, so a page missing from here would be generated, linked from the
    catalog, and then quietly pushed to the end of its track on every build.
    """
    listed = [p for pairs in INSERT_AFTER.values() for _a, ps in pairs for p in ps]
    if len(listed) != len(set(listed)):
        raise SystemExit("arch_topics.INSERT_AFTER lists a page twice")
    real = {_path(t) for t in TOPICS}
    missing = real - set(listed)
    extra = set(listed) - real
    if missing:
        raise SystemExit("arch_topics: not placed in a sequence: %s"
                         % ", ".join(sorted(missing)))
    if extra:
        raise SystemExit("arch_topics.INSERT_AFTER names unknown pages: %s"
                         % ", ".join(sorted(extra)))


_check_order()
