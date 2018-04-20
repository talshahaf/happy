package com.appy;

import android.content.Context;
import android.content.Intent;

/**
 * Created by Tal on 30/12/2017.
 */

interface TestInterface
{
    Object action(Object i) throws Throwable;
}

interface BroadcastInterface
{
    void onReceive(Context context, Intent intent);
}

interface WidgetUpdateListener
{
    String onCreate(int widgetId);
    String onUpdate(int widgetId, String views);
    void onDelete(int widgetId);
    Object[] onItemClick(int widgetId, String views, int collectionId, int position);
    String onClick(int widgetId, String views, int id);
    String onTimer(int timerId, int widgetId, String views, String data);
    String onPost(int widgetId, String views, String data);
    void wipeStateRequest();
    void importFile(String path);
    void deimportFile(String path);
}

interface RunnerListener
{
    void onLine(String line);
    void onExited(Integer code);
}

interface StatusListener
{
    void onStartupStatusChange();
    void onPythonFileStatusChange();
}
