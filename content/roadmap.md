# Content roadmap

Topics proposed but not yet built, with what each module's visualisation
would show. Kept here rather than in a chat log so the next batch does not
start from scratch.

Counts are from the catalog at the time of writing; `python3 -c "import sys;
sys.path.insert(0,'tools'); from lib_catalog import counts; print(counts())"`
gives the current ones.

---

## Done

**Python: 12 -> 46.** Tier 1, 2 and 3 all built, generated from
`tools/python_topics.py`. Adding a 35th topic is one entry there plus a line
in `tools/sequence.py`.

**Database: 22 -> 42.** Tiers 1 and 2 are complete, generated from
`tools/db_topics.py`. Most modules run real SQLite in the page through
`assets/vizlearn-sql.js` - the same engine as /sql-lab/, seeded per module, so
the error messages are the database's own. Isolation levels, deadlocks, MVCC,
replication lag and CAP step through a scripted two-transaction schedule
instead, because one connection cannot demonstrate two. The document,
key-value and graph modules lean on SQLite's JSON1 functions and recursive
CTEs, which the in-page engine has.

**Computer Vision: 20 -> 40.** Tiers 1 and 2 are complete, generated from
`tools/cv_topics.py` with the arithmetic in `assets/vizlearn-cv.js`. Eight are
image operations driven by the pixel harness; receptive field and 1x1
convolutions are SVG diagrams driven by the same controls, because neither has
an image to show. Tier 2 added four more image operations (template matching, Harris, ViT
patching, the segmentation taxonomy) and six diagrams. Adding a twenty-first is
one entry in `cv_topics.py`, a line in `tools/sequence.py`, and - if the harness
lacks the operation - one function in `OPS` or `DIAGRAMS`.

**Deep Learning: 32 -> 42.** Tier 1 is complete, generated from
`tools/dl_topics.py` with the demonstrations in `assets/vizlearn-dl.js`. The
track was thorough on training mechanics and stopped at a dense network;
autoencoders, VAEs, GANs, diffusion, contrastive learning and beam search had
no page anywhere on the site. Attention, transfer learning, distillation and
augmentation are deliberately absent - NLP, Computer Vision and Gen AI already
own those.

**Maths: 27 -> 47.** Tiers 1 and 2 are complete, generated from `tools/math_topics.py`
with the demonstrations in `assets/vizlearn-math.js`. These are demonstrations
rather than simulations - nothing is fitted, and the arithmetic is the subject:
the SVD is a real decomposition of the matrix on screen, the central limit page
really resamples the population it draws, and the convexity page really runs
gradient descent and really gets stuck in a local minimum.

The plotter, the seeded RNG and the numeric helpers moved out of
`vizlearn-ml.js` into `assets/vizlearn-plot.js` so both harnesses share one
copy. Tier 2 added the inference trio (confidence intervals, p-values, the two
error rates), QR and Cholesky, matrix calculus, Lagrange multipliers, Jensen,
Markov chains and combinatorics.

**Machine Learning: 25 -> 45.** Tiers 1 and 2 are complete, generated from
`tools/ml_topics.py` with the simulations in `assets/vizlearn-ml.js`. Every
score is computed in the browser from data generated in the browser, so the
leakage module genuinely selects features with the labels in hand and genuinely
reports the inflated number that follows.

## Computer Vision (20)

Twelve of the twenty modules are CNN internals. What is missing is the layer
below - classical image processing, the most visual subject on the site - and
the layer above, modern architectures.

### Tier 1 - the missing foundation

| Topic | What you drive |
|---|---|
| Convolution kernels by hand | Edit a 3x3 matrix; blur, sharpen, emboss, Sobel appear live |
| Thresholding | One slider splits to binary; watch detail collapse |
| Histograms and equalisation | Histogram beside the image, both updating as contrast stretches |
| Blur: Gaussian vs median vs bilateral | One noisy image, three filters, edges kept or lost |
| Erosion and dilation | Structuring element grows and shrinks shapes; open/close as combinations |
| Colour spaces: RGB vs HSV | Drag hue and saturation; see why HSV makes colour selection trivial |
| Resizing and interpolation | Nearest vs bilinear vs bicubic on a zoomed patch |
| Affine transforms | Edit the 2x3 matrix: rotate, scale, shear, translate |
| Receptive field | Trace one output pixel back to the input region it sees |
| 1x1 convolutions | Channel mixing with no spatial extent |

All ten are built.

### Tier 2 - architectures and detection

All ten are built.

- Depthwise separable convolution (parameter saving, counted live)
- Dilated / atrous convolution
- Global average pooling vs flatten
- Anchor boxes (the piece before the existing IoU/NMS module)
- mAP for object detection
- Template matching
- Harris corners and keypoints
- Vision Transformer patches
- Grad-CAM
- Instance vs semantic vs panoptic segmentation

---

## Database (22)

Query coverage is strong - joins, CTEs, window functions, execution order.
Almost nothing on schema design, concurrency, or the NoSQL side beyond one
intro page.

### Tier 1 - design and concurrency

| Topic | What you drive |
|---|---|
| Primary and foreign keys | Insert a row that breaks a reference; watch it rejected |
| Constraints: UNIQUE, CHECK, NOT NULL | Try the violating insert, see which constraint fires |
| Aggregate functions | COUNT/SUM/AVG/MIN/MAX over a live table, with the NULL trap |
| EXISTS vs IN vs JOIN | One question three ways, with row counts and plans compared |
| Self-joins | A table joined to itself: employees and managers |
| Recursive CTEs | Watch the recursion build a hierarchy one level at a time |
| EXPLAIN and query plans | Read the plan, add an index, watch the plan change |
| Composite and covering indexes | Column order matters: the query that uses it and the one that cannot |
| Isolation levels | Two transactions side by side producing dirty/non-repeatable/phantom reads |
| Deadlocks | Two transactions taking locks in opposite order |

All ten are built.

### Tier 2 - scale, NoSQL, safety

All ten are built.

- MVCC: how readers avoid blocking writers
- Partitioning by range or hash
- Sharding (distinct from the Gen AI retrieval-sharding module)
- Replication, read replicas and replication lag
- CAP theorem
- Document model: the same data as rows vs as documents
- Key-value and graph models
- OLTP vs OLAP, and columnar storage
- Star schema: facts and dimensions
- SQL injection and parameterised queries

---

## Machine Learning (25)

Model coverage is good; nearly all the classical algorithms are there. What is
thin is the workflow around them - preprocessing, leakage, tuning,
interpretation - which is where real projects fail.

### Tier 1 - the workflow

| Topic | What you drive |
|---|---|
| Feature scaling | StandardScaler vs MinMaxScaler; KNN and SVM move, trees do not |
| Data leakage | Scale before the split and watch accuracy jump to a lie |
| Handling missing values | Drop vs mean vs median vs indicator, scored against each other |
| Outliers | Move one point, watch a linear fit swing |
| Pipelines | The correct order, with the leaky version beside it |
| Precision, recall and F1 | Move the threshold, watch the trade-off |
| Precision-Recall vs ROC | Same model, imbalanced data, why ROC flatters it |
| Threshold tuning | 0.5 is a default, not a decision |
| Grid search vs random search | Same budget; random wins in high dimensions |
| Learning curves | Train/validation gap diagnosing bias vs variance |

All ten are built.

### Tier 2 - models and interpretation

All ten are built.

- DBSCAN: density clustering, shapes k-means cannot find
- Hierarchical clustering and dendrograms
- Choosing k: elbow and silhouette
- Gaussian Mixture Models
- t-SNE and UMAP beside the existing PCA
- Feature and permutation importance
- SHAP and partial dependence
- Probability calibration
- Isolation Forest
- Stacking and voting ensembles (bagging and boosting already exist)

---

## What is left

Every tier in this file is built. The tracks now run from 37 (NLP) to 49
(Interview), and the next expansion should start from a fresh gap analysis
rather than from this document.

## Overlaps to respect

- ML feature scaling vs Deep Learning's *Feature Scaling in Neural Networks* -
  keep the ML one tabular: scikit-learn scalers, tree models unaffected.
- Database sharding vs Gen AI's *Distributed Retrieval and Sharding* - that
  one is about vector retrieval; this one is about tables.
- The dsa/ Python labs and the interview/ track already cover Python
  internals and performance. Language tracks stay on how to write the thing.
