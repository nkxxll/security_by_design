import os
import sys
import subprocess

running_threads = []


def run_program_in_thread(programm_arguments=["echo", "No", "arguments", "given"]):
    process_output = subprocess.run(
        programm_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output_string = process_output.stdout.decode("utf-8")
    error_log = process_output.stderr.decode("utf-8")
    return (output_string, error_log)


def run_program_in_seperate_thread(
    programm_arguments=["echo", "No", "arguments", "given"]
):
    new_thread = threading.Thread(
        target=run_program_in_thread, args=[programm_arguments]
    )
    running_threads.append(new_thread)
    new_thread.start()


def close_all_threads():
    for thread in running_threads:
        thread.join()


def __main__():
    run_program_in_seperate_thread(["cd", ".\\msbDatabase\\", "&&", "npm", "start"])


if __name__ == "__main__":
    __main__()
