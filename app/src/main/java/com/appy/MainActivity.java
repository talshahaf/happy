package com.appy;

import android.support.v4.app.FragmentTransaction;
import android.support.annotation.NonNull;
import android.support.v4.app.Fragment;
import android.content.Intent;
import android.os.Handler;
import android.support.design.widget.NavigationView;
import android.support.v4.app.FragmentManager;
import android.support.v7.app.ActionBar;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.AppCompatActivity;

import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.util.Pair;
import android.view.Gravity;
import android.view.MenuItem;
import java.util.HashMap;

public class MainActivity extends AppCompatActivity
{
    private DrawerLayout drawer;
    private Toolbar toolbar;
    private NavigationView navView;
    private HashMap<Integer, Pair<Class<?>, MyFragment>> fragments = new HashMap<>();
    public static final String FRAGMENT_TAG = "FRAGMENT";

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        fragments.put(R.id.navigation_control, new Pair<Class<?>, MyFragment>(ControlFragment.class, null));
        fragments.put(R.id.navigation_logcat, new Pair<Class<?>, MyFragment>(LogcatFragment.class, null));
        fragments.put(R.id.navigation_pip, new Pair<Class<?>, MyFragment>(PipFragment.class, null));
        //fragments.put(R.id.navigation_files, new Pair<Class<?>, MyFragment>(FilesFragment.class, null));

        // Set a Toolbar to replace the ActionBar.
        toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        ActionBar actionBar = getSupportActionBar();
        actionBar.setDisplayHomeAsUpEnabled(true);
        actionBar.setHomeButtonEnabled(true);
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
                MyFragment fragment = (MyFragment)getSupportFragmentManager().findFragmentByTag(FRAGMENT_TAG);
                MenuItem menuItem = navView.getMenu().findItem(fragment.getMenuId());
                menuItem.setChecked(true);
                setTitle(menuItem.getTitle());
            }
        });

        startService(new Intent(this, Widget.class));

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

    public void selectDrawerItem(@NonNull MenuItem menuItem)
    {
        // Create a new fragment and specify the fragment to show based on nav item clicked
        int itemId = menuItem.getItemId();

        Pair<Class<?>, MyFragment> cls = fragments.get(itemId);
        if (cls == null)
        {
            itemId = R.id.navigation_control;
            cls = fragments.get(itemId);
        }

        MyFragment fragment = cls.second;
        if (fragment == null)
        {
            try
            {
                fragment = (MyFragment) cls.first.newInstance();
                fragment.setMenuId(itemId);
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }

            fragments.put(itemId, new Pair<Class<?>, MyFragment>(cls.first, fragment));
        }

        if (fragment == null)
        {
            return;
        }

        MyFragment prev = (MyFragment) getSupportFragmentManager().findFragmentByTag(FRAGMENT_TAG);

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

            transaction.replace(R.id.container, fragment, FRAGMENT_TAG);
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


}
