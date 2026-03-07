"""Composite block — CI/CD Pipelines & Render Deployment."""

import streamtex as stx
from streamtex import st_include

bck_ci_workflow = stx.load_atomic_block("bck_ci_workflow", __file__)
bck_publish_workflow = stx.load_atomic_block("bck_publish_workflow", __file__)
bck_render_deployment = stx.load_atomic_block("bck_render_deployment", __file__)


class BlockStyles:
    pass


bs = BlockStyles


def build():
    st_include(bck_ci_workflow)
    st_include(bck_publish_workflow)
    st_include(bck_render_deployment)
