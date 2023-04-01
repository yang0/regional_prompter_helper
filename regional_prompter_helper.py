import copy
import math
import os
import random
import sys
import traceback
import shlex

import modules.scripts as scripts
import gradio as gr

from modules import sd_samplers
from modules.processing import Processed, process_images
from PIL import Image
from modules.shared import opts, cmd_opts, state


def process_string_tag(tag):
    return tag


def process_int_tag(tag):
    return int(tag)


def process_float_tag(tag):
    return float(tag)


def process_boolean_tag(tag):
    return True if (tag == "true") else False



def load_prompt_file(file):
    if file is None:
        lines = []
    else:
        lines = [x.strip() for x in file.decode('utf8', errors='ignore').split("\n")]

    return None, "\n".join(lines), gr.update(lines=7)


class Script(scripts.Script):
    def title(self):
        return "regional prompter helper"

    def ui(self, is_img2img):       
        prompt_txt1 = gr.Textbox(label="Start prompt inputs", lines=1, elem_id=self.elem_id("prompt_txt"))
        prompt_txt2 = gr.Textbox(label="End prompt inputs", lines=1, elem_id=self.elem_id("prompt_txt"))
        image_number = gr.Number(label="region count", value=20)


        # We start at one line. When the text changes, we jump to seven lines, or two lines if no \n.
        # We don't shrink back to 1, because that causes the control to ignore [enter], and it may
        # be unclear to the user that shift-enter is needed.
        # prompt_txt.change(lambda tb: gr.update(lines=7) if ("\n" in tb) else gr.update(lines=2), inputs=[prompt_txt], outputs=[prompt_txt])
        return [prompt_txt1, prompt_txt2, image_number]

    def run(self, p, prompt_txt1: str, prompt_txt2: str, image_number: int):
        p.do_not_save_grid = True

        job_count = 0
        jobs = []

        state.job_count = job_count

        images = []
        all_prompts = []
        infotexts = []

        prompt_txt1 += " BREAK "
        prompt_txt2 += " BREAK "

        result = ""
        image_number = int(image_number)
        for i in range(image_number):
            a_count = image_number - i
            b_count = i
            result += p.prompt + " BREAK " + prompt_txt1 * a_count + prompt_txt2 * b_count
            result = result.rstrip("BREAK ")

            jobs.append({"prompt":result})
            job_count += 1
            result = ""


        state.job_count = job_count            

        for n, args in enumerate(jobs):
            state.job = f"{state.job_no + 1} out of {state.job_count}"

            copy_p = copy.copy(p)
            for k, v in args.items():
                print(v)
                setattr(copy_p, k, v)

            proc = process_images(copy_p)
            images += proc.images
            
            all_prompts += proc.all_prompts
            infotexts += proc.infotexts

        return Processed(p, images, p.seed, "", all_prompts=all_prompts, infotexts=infotexts)
