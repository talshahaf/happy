package com.appy;

import android.content.ComponentName;
import android.content.Context;
import android.content.ServiceConnection;
import android.os.IBinder;
import android.support.v4.app.FragmentTransaction;
import android.support.annotation.NonNull;
import android.support.v4.app.Fragment;
import android.content.Intent;
import android.support.design.widget.NavigationView;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.ActionBar;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;

import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.util.Pair;
import android.view.Gravity;
import android.view.MenuItem;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity implements StatusListener
{
    private DrawerLayout drawer;
    private Toolbar toolbar;
    private NavigationView navView;
    private HashMap<Integer, Pair<Class<?>, Fragment>> fragments = new HashMap<>();
    public static final String FRAGMENT_TAG = "FRAGMENT";

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        fragments.put(R.id.navigation_control, new Pair<Class<?>, Fragment>(ControlFragment.class, null));
        fragments.put(R.id.navigation_logcat, new Pair<Class<?>, Fragment>(LogcatFragment.class, null));
        fragments.put(R.id.navigation_pip, new Pair<Class<?>, Fragment>(PipFragment.class, null));
        fragments.put(R.id.navigation_files, new Pair<Class<?>, Fragment>(FilesFragment.class, null));
        fragments.put(R.id.navigation_configs, new Pair<Class<?>, Fragment>(ConfigsFragment.class, null));
        fragments.put(R.id.navigation_crash, new Pair<Class<?>, Fragment>(CrashFragment.class, null));
        fragments.put(R.id.navigation_settings, new Pair<Class<?>, Fragment>(SettingsFragment.class, null));

        // Set a Toolbar to replace the ActionBar.
        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        ActionBar actionBar = getSupportActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true);
        actionBar.setHomeButtonEnabled(true);
        actionBar.setHomeAsUpIndicator(R.drawable.ic_menu_24dp);
        // Find our drawer view
        drawer = findViewById(R.id.drawer_layout);
        navView = findViewById(R.id.nav_view);
        // Setup drawer view
        navView.setNavigationItemSelectedListener(
                new NavigationView.OnNavigationItemSelectedListener() {
                    @Override
                    public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
                        Log.d("APPY", "onNavigationItemSelected");
                        selectDrawerItem(menuItem);
                        return true;
                    }
                });


        getSupportFragmentManager().addOnBackStackChangedListener(new FragmentManager.OnBackStackChangedListener()
        {
            @Override
            public void onBackStackChanged()
            {
                MyFragmentInterface fragment = (MyFragmentInterface)getSupportFragmentManager().findFragmentByTag(FRAGMENT_TAG);
                MenuItem menuItem = navView.getMenu().findItem(fragment.getMenuId());
                if(menuItem != null)
                {
                    menuItem.setChecked(true);
                    setTitle(menuItem.getTitle());
                }
            }
        });

        startService(new Intent(this, Widget.class));
        doBindService();

        selectDrawerItem(navView.getMenu().getItem(0));
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // The action bar home/up action should open or close the drawer.
        switch (item.getItemId()) {
            case android.R.id.home:
                drawer.openDrawer(Gravity.START);
                return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
    }

    public void selectDrawerItem(@NonNull MenuItem menuItem)
    {
        // Create a new fragment and specify the fragment to show based on nav item clicked
        int itemId = menuItem.getItemId();

        Pair<Class<?>, Fragment> cls = fragments.get(itemId);
        if (cls == null)
        {
            itemId = R.id.navigation_control;
            cls = fragments.get(itemId);
        }

        MyFragmentInterface fragment = (MyFragmentInterface)cls.second;
        if (fragment == null)
        {
            try
            {
                fragment = (MyFragmentInterface)cls.first.newInstance();
                fragment.setMenuId(itemId);
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }

            fragments.put(itemId, new Pair<Class<?>, Fragment>(cls.first, (Fragment)fragment));
        }

        if (fragment == null)
        {
            return;
        }

        MyFragmentInterface prev = (MyFragmentInterface) getSupportFragmentManager().findFragmentByTag(FRAGMENT_TAG);

        if (prev != fragment)
        {
            if(prev != null)
            {
                prev.onHide();
            }

            // Insert the fragment by replacing any existing fragment
            FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
            transaction.setCustomAnimations(
                    R.animator.slide_in_from_right, R.animator.slide_out_to_left,
                    R.animator.slide_in_from_left, R.animator.slide_out_to_right);
            transaction.setPrimaryNavigationFragment((Fragment)fragment);
            transaction.replace(R.id.container, (Fragment)fragment, FRAGMENT_TAG);
            if(prev != null)
            {
                transaction.addToBackStack(null);
            }
            transaction.commit();
            fragment.onShow();
        }

        // Highlight the selected item has been done by NavigationView
        menuItem.setChecked(true);
        // Set action bar title
        setTitle(menuItem.getTitle());
        // Close the navigation drawer
        drawer.closeDrawers();
    }

    public Widget widgetService = null;

    private ServiceConnection mConnection = new ServiceConnection() {
        public void onServiceConnected(ComponentName className, IBinder service) {
            widgetService = ((Widget.LocalBinder)service).getService();
            widgetService.setStatusListener(MainActivity.this);
            for(Pair<Class<?>, Fragment> frag : fragments.values())
            {
                if(frag.second != null)
                {
                    ((MyFragmentInterface)frag.second).onBound();
                }
            }
        }

        public void onServiceDisconnected(ComponentName className) {
            widgetService = null;
        }
    };

    void doBindService() {
        Intent bindIntent = new Intent(this, Widget.class);
        bindIntent.putExtra(Constants.LOCAL_BIND_EXTRA, true);
        bindService(bindIntent, mConnection, Context.BIND_AUTO_CREATE);
    }

    void doUnbindService() {
        if (widgetService != null) {
            widgetService.setStatusListener(null);
            unbindService(mConnection);
            widgetService = null;
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        doUnbindService();
    }

    @Override
    public void onStartupStatusChange()
    {
        Fragment fragment = fragments.get(R.id.navigation_control).second;
        if(fragment != null)
        {
            ((ControlFragment)fragment).onStartupStatusChange();
        }
    }

    @Override
    public void onPythonFileStatusChange()
    {
        Fragment fragment = fragments.get(R.id.navigation_files).second;
        if(fragment != null)
        {
            ((FilesFragment)fragment).onPythonFileStatusChange();
        }
    }
}
