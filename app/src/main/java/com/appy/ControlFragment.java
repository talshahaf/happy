package com.appy;

import android.support.v4.app.Fragment;
import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;

/**
 * Created by Tal on 19/03/2018.
 */

public class ControlFragment extends MyFragment
{
    Button clearWidgets;
    Button clearTimers;
    Button clearState;
    Button restart;

    Handler handler;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View layout = inflater.inflate(R.layout.control_fragment, container, false);

        clearWidgets = layout.findViewById(R.id.clear_widgets);
        clearTimers = layout.findViewById(R.id.clear_timers);
        clearState = layout.findViewById(R.id.clear_state);
        restart = layout.findViewById(R.id.restart);

        handler = new Handler();

        clearWidgets.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                clickHandler(v, Widget.ACTION_CLEAR, "widgets");
            }
        });

        clearTimers.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                clickHandler(v, Widget.ACTION_CLEAR, "timers");
            }
        });

        clearState.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                clickHandler(v, Widget.ACTION_CLEAR, "state");
            }
        });

        restart.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                clickHandler(v, Widget.ACTION_RESTART, null);
            }
        });

        return layout;
    }

    public void clickHandler(final View v, String action, String flag)
    {
        Intent intent = new Intent(getActivity(), Widget.class);
        intent.setAction(action);
        if(flag != null)
        {
            intent.putExtra(flag, true);
        }
        getActivity().startService(intent);
        v.setEnabled(false);
        handler.postDelayed(new Runnable()
        {
            @Override
            public void run()
            {
                v.setEnabled(true);
            }
        }, 1000);
    }
}
