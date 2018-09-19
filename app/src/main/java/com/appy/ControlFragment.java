package com.appy;

import android.os.Bundle;
import android.os.Handler;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.ProgressBar;

/**
 * Created by Tal on 19/03/2018.
 */

public class ControlFragment extends MyFragment
{
    ProgressBar startupProgress;
    ImageView startupStatus;
    Button clearWidgets;
    Button clearTimers;
    Button clearState;
    Button restart;

    Handler handler;

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {

        View layout = inflater.inflate(R.layout.fragment_control, container, false);

        startupProgress = layout.findViewById(R.id.startup_progress);
        startupStatus = layout.findViewById(R.id.startup_status);
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
                getWidgetService().resetWidgets();
                debounce(v);
            }
        });

        clearTimers.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                getWidgetService().cancelAllTimers();
                debounce(v);
            }
        });

        clearState.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(View v)
            {
                getWidgetService().resetState();
                debounce(v);
            }
        });

        restart.setOnClickListener(new View.OnClickListener()
        {
            @Override
            public void onClick(final View v)
            {
                getWidgetService().restart();
                debounce(v);
            }
        });

        onStartupStatusChange();

        return layout;
    }

    public void debounce(final View v)
    {
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

    public void onBound()
    {
        onStartupStatusChange();
    }

    public void onStartupStatusChange()
    {
        if(getWidgetService() == null)
        {
            return;
        }
        switch(getWidgetService().getStartupState())
        {
            case IDLE:
                startupStatus.setImageResource(R.drawable.idle_indicator);
                startupProgress.setVisibility(View.INVISIBLE);
                startupStatus.setVisibility(View.VISIBLE);
                break;
            case RUNNING:
                startupProgress.setVisibility(View.VISIBLE);
                startupStatus.setVisibility(View.INVISIBLE);
                break;
            case ERROR:
                startupStatus.setImageResource(R.drawable.error_indicator);
                startupProgress.setVisibility(View.INVISIBLE);
                startupStatus.setVisibility(View.VISIBLE);
                break;
            case COMPLETED:
                startupStatus.setImageResource(R.drawable.success_indicator);
                startupProgress.setVisibility(View.INVISIBLE);
                startupStatus.setVisibility(View.VISIBLE);
                break;
        }
    }
}
