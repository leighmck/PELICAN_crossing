# -*- coding: utf-8 -*-
# Copyright (c) 2019, Leigh McKenzie
# All rights reserved.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import enum
import logging
import sys
import tkinter

import statechart
from statechart import display


class Light(enum.IntEnum):
    GREEN = 0,
    YELLOW = 1,
    RED = 2


def call_button():
    """Dispatch the call button pressed event.

    Print the state chart state.
    This event will be ignored unless the active state(s) are listening for it.
    """
    sc.dispatch(call_button_pressed)
    print(sc)


def dispatch(event):
    sc.dispatch(event=statechart.Event(name=event))


window = tkinter.Tk()

sc = statechart.Statechart(name="PELICAN-crossing")
call_button_pressed = statechart.Event("call-button-pressed")
crossing_timeout = statechart.Event("crossing-timeout")

window.title("PELICAN crossing example")
window.geometry('400x200')
state_text = tkinter.StringVar(value="")
state_label = tkinter.Label(window, textvariable=state_text)
state_label.grid(column=0, row=0)
btn = tkinter.Button(window, text="Call Button", command=call_button)
btn.grid(column=1, row=0)


class CrossingState(statechart.State):
    """Generic crossing state used to update the state label text and fire a timeout event after 5 seconds."""

    def __init__(self, name, context):
        super().__init__(name=name, context=context)

    def entry(self, event):
        state_text.set(self.name)
        window.after(5000, dispatch, "crossing-timeout")


class Go(CrossingState):
    """Go state, handles caching of the call-button pressed state."""

    def __init__(self, context):
        super().__init__(name="Go", context=context)
        self.is_call_button_pressed = False

    def entry(self, event):
        super().entry(event)
        self.is_call_button_pressed = False

    def handle_internal(self, event):
        if event.name == "call-button-pressed":
            self.is_call_button_pressed = True


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Step 1 - Identify the states

    # Root context
    root_initial = statechart.InitialState(context=sc)
    traffic = statechart.CompositeState(name="Traffic", context=sc)
    pedestrian = statechart.CompositeState(name="Pedestrian", context=sc)

    # Traffic context
    traffic_initial = statechart.InitialState(context=traffic)
    go = Go(context=traffic)
    go_await_pedestrian = CrossingState(name="Go-Await-Pedestrian", context=traffic)
    caution = CrossingState(name="Caution", context=traffic)
    stop = CrossingState(name="Stop", context=traffic)
    traffic_final = statechart.FinalState(context=traffic)

    # Pedestrian context
    pedestrian_initial = statechart.InitialState(context=pedestrian)
    walk = CrossingState(name="Walk", context=pedestrian)
    clear_crossing = CrossingState(name="Clear-Crossing", context=pedestrian)
    dont_walk = CrossingState(name="Don't-Walk", context=pedestrian)
    pedestrian_final = statechart.FinalState(context=pedestrian)

    # Step 2 - Identify the events

    # Step 3 - Identify the transitions between states

    # Root context
    # Traffic is the initial state
    # Transition to pedestrian mode when traffic is finished. Likewise, transition to traffic when pedestrian mode
    # is finished.
    statechart.Transition(start=root_initial, end=traffic)
    statechart.Transition(start=traffic, end=pedestrian)
    statechart.Transition(start=pedestrian, end=traffic)

    # Traffic context
    # Go is the initial state
    # Let traffic flow initially by deferring handling of the call button.
    # After this timeout, if the call button was pressed, go straight to the caution state.
    # Otherwise, wait for the call button and transition to caution immediately when pressed.
    # Transition from caution to stop after the set timeout.
    statechart.Transition(start=traffic_initial, end=go)

    # Notice how there are two transitions from the Go state based triggered by the crossing_timeout event.
    # Transitions with guards will be tested first.
    # The second transition will always fire - just like an if, elif, else sequence.
    statechart.Transition(start=go, end=caution, event=crossing_timeout, guard=lambda: go.is_call_button_pressed)
    statechart.Transition(start=go, end=go_await_pedestrian, event=crossing_timeout)  # Else
    statechart.Transition(start=go_await_pedestrian, end=caution, event=call_button_pressed)
    statechart.Transition(start=caution, end=stop, event=crossing_timeout)
    statechart.Transition(start=stop, end=traffic_final, event=crossing_timeout)

    # Pedestrian context
    # Walk is the initial state.
    # Transition from walk to clear to don't walk after the set timeouts.
    # Finalise the pedestrian state to let the state machine revert to traffic mode.
    statechart.Transition(start=pedestrian_initial, end=walk)
    statechart.Transition(start=walk, end=clear_crossing, event=crossing_timeout)
    statechart.Transition(start=clear_crossing, end=dont_walk, event=crossing_timeout)
    statechart.Transition(start=dont_walk, end=pedestrian_final, event=crossing_timeout)

    # Step 4 - Start the state machine - dispatch events to trigger state changes.

    print("Display statechart using https://www.planttext.com/")
    print(display.Display().plantuml(statechart=sc))

    sc.start()

    window.mainloop()


if __name__ == "__main__":
    main()
